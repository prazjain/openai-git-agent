
import asyncio
import os
from dotenv import load_dotenv
from remote_repos import githubrepo

import local_repo
import local_fs

#from remote_repos.githubrepo import get_instance, get_repo, create_branch
#from local_repo import clone_repo
#from local_fs import get_src_and_task_files, read_task_file, generate_random_filename
#from agentic import generate_solution

import agentic

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")
openai_key = os.getenv("OPENAI_API_KEY")
github = githubrepo.get_instance()

def main():
    start_repo_name = "prazjain/genai-scratch-repo"
    start_branch_name = "python/genai-agent-task"
    random_suffix = local_fs.generate_random_filename()
    solution_branch_name = f"{start_branch_name}-agent-solution-#iteration-{random_suffix}"
    solution_file_path = "./agent-task/solution.py"
    local_repo_dir = os.path.join(os.getcwd(), "agent-task")

    remote_repo = githubrepo.get_repo(github, repo_name=start_repo_name)
    remote_branch = remote_repo.get_branch(start_branch_name)

    local_fs.delete_dir(local_repo_dir)
    local_repo_obj = local_repo.clone_repo(remote_repo.clone_url, local_repo_dir, branch_name=start_branch_name)

    src_files, task_files = local_fs.get_src_and_task_files(local_repo_dir)
    #src_files = [os.path.join('.', 'agent-task', file) for file in src_files if not file.endswith(".pyc")]
    #task_files = [os.path.join('.', 'agent-task', file) for file in task_files if not file.endswith(".pyc")]
    print('\n'.join(src_files))
    print('\n'.join(task_files))
    task_file = task_files[0]
    task_description, error = local_fs.read_file(os.path.join('.', 'agent-task', task_file))
    if error:
        print(error)
        return
    code_solution, iteration = asyncio.run(agentic.generate_solution(task_description))
    #print(code_solution.final_output.code)
    iteration=1

    solution_branch_name = solution_branch_name.replace("#iteration", str(iteration))
    solution_branch_head = local_repo.create_branch(local_dir=local_repo_dir,branch_name=solution_branch_name)

    local_fs.write_file(solution_file_path, code_solution.final_output.code)

    task_file_dest = task_file.replace("genai-todo", "genai-completed")
    print(task_file_dest)
    import pathlib
    pathlib.Path(os.path.join('.', 'agent-task', task_file_dest)).parent.mkdir(parents=True, exist_ok=True)
    local_repo.move_files(local_dir=local_repo_dir, src_file_paths=[task_file], dest_file_paths=[task_file_dest])
    local_repo.commit_changes(local_dir=local_repo_dir, commit_message=f"Add solution for task {iteration}", files=[solution_file_path])
    local_repo.push_changes(local_dir=local_repo_dir, branch_name=solution_branch_name)
    
    print(f"Pushed solution to branch {solution_branch_name}")

    githubrepo.create_pull_request(
        github,
        repo_name=start_repo_name,
        title=f"Add solution for task {iteration}",
        body="This PR adds the solution for the task.",
        head=solution_branch_name,
        base=start_branch_name,
    )
    print(f"Pull request created for branch {solution_branch_name}")


if __name__ == "__main__":
    main()