
import asyncio
import os
from dotenv import load_dotenv
from remote_repos import github_facade, githubrepo

import local_repo
import local_fs

import agentic
import logging 
import logging_config

logger = logging.getLogger(__name__)

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")
openai_key = os.getenv("OPENAI_API_KEY")
github = githubrepo.get_instance()

def run_agent(task_description, mock=False):
    if mock:
        return get_mock_output()
    code_solution, iteration = asyncio.run(agentic.generate_solution(task_description))
    return code_solution.final_output.code, iteration

def get_mock_output():
    content, error = local_fs.read_file(os.path.join(os.getcwd(), "agent-task", "mock", "solution.py"))
    return content, 1

def main():
    start_repo_name = "prazjain/genai-scratch-repo"
    start_branch_name = "python/genai-agent-task"
    random_suffix = local_fs.generate_random_filename()
    solution_branch_name = f"{start_branch_name}-agent-solution-#iteration-{random_suffix}"
    solution_file_path = "solution.py"
    local_repo_dir = os.path.join(os.getcwd(), "agent-task")

    ghub_repo = github_facade.GithubRepoFacade(repo_name=start_repo_name)

    local_fs.delete_dir(local_repo_dir)
    local_repo_obj = local_repo.clone_repo(ghub_repo.get_repo().clone_url, local_repo_dir, branch_name=start_branch_name)

    src_files, task_files = local_fs.get_src_and_task_files(local_repo_dir)

    task_file = task_files[0]
    task_description, error = local_fs.read_file(os.path.join('.', 'agent-task', task_file))
    if error:
        logger.error(error)
        return
    code_solution, iteration = run_agent(task_description, mock=True)
    #logger.debug(code_solution.final_output.code)
    
    solution_branch_name = solution_branch_name.replace("#iteration", str(iteration))
    solution_branch_head = local_repo.create_branch(local_dir=local_repo_dir,branch_name=solution_branch_name)

    local_fs.write_file(os.path.join('agent-task', solution_file_path), code_solution)
    logger.debug(f'About to add solution file to repo {solution_file_path} ...')
    local_repo.add_files(local_dir=local_repo_dir, file_paths=[solution_file_path])
    logger.debug('Added solution file to repo ...')
    task_file_dest = task_file.replace("genai-todo", "genai-completed")
    logger.debug(task_file_dest)
    import pathlib
    pathlib.Path(os.path.join('.', 'agent-task', task_file_dest)).parent.mkdir(parents=True, exist_ok=True)
    local_repo.move_files(local_dir=local_repo_dir, src_file_paths=[task_file], dest_file_paths=[task_file_dest])
    local_repo.commit_changes(local_dir=local_repo_dir, commit_message=f"Add solution for task {iteration}", files=[solution_file_path])
    local_repo.push_changes(local_dir=local_repo_dir, branch_name=solution_branch_name)
    
    logger.info(f"Pushed solution to branch {solution_branch_name}")

    pr_url = ghub_repo.create_pull_request(
        title=f"Add solution for task {iteration}",
        body="This PR adds the solution for the task.",
        head=solution_branch_name,
        base=start_branch_name,
    )
    logger.info(f"Pull request created for branch {solution_branch_name} {pr_url}")

if __name__ == "__main__":
    main()