'''
Operations related to local repositories.
This module provides functions to manage local repositories, including
creating, deleting, and checking the status of repositories.
'''
import os
from git import Repo

def clone_repo(repo_url, local_dir, branch_name="main"):
    """
    Clone a repository from a given URL to a local directory.
    
    Args:
        repo_url (str): The URL of the repository to clone.
        local_dir (str): The local directory where the repository will be cloned.
    
    Returns:
        Repo: The cloned repository object.
    """
    if os.path.exists(local_dir):
        print(f"Directory {local_dir} already exists, choose new path for clone.")
        return None
    else:
        print(f"Cloning repository from {repo_url} to {local_dir}.")
        repo = Repo.clone_from(repo_url, local_dir, branch=branch_name)
    
    return repo
def delete_repo(local_dir):
    """
    Delete a local repository directory.
    Args:
        local_dir (str): The local directory of the repository to delete.
    """
    if os.path.exists(local_dir):
        print(f"Deleting repository at {local_dir}.")
        os.rmdir(local_dir)
    else:
        print(f"Directory {local_dir} does not exist.")
def check_repo_status(local_dir):
    """
    Check the status of a local repository.
    
    Args:
        local_dir (str): The local directory of the repository to check.
    
    Returns:
        str: The status of the repository.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        status = repo.git.status()
        return status
    else:
        return f"Directory {local_dir} does not exist."
def get_repo_info(local_dir):
    """
    Get information about a local repository.
    
    Args:
        local_dir (str): The local directory of the repository.
    
    Returns:
        dict: A dictionary containing repository information.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        info = {
            "branch": repo.active_branch.name,
            "commit": repo.head.commit.hexsha,
            "author": repo.head.commit.author.name,
            "message": repo.head.commit.message,
        }
        return info
    else:
        return f"Directory {local_dir} does not exist."
def list_branches(local_dir):
    """
    List all branches in a local repository.
    
    Args:
        local_dir (str): The local directory of the repository.
    
    Returns:
        list: A list of branch names.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        branches = [branch.name for branch in repo.branches]
        return branches
    else:
        return f"Directory {local_dir} does not exist."
def checkout_branch(local_dir, branch_name):
    """
    Checkout a specific branch in a local repository.
    
    Args:
        local_dir (str): The local directory of the repository.
        branch_name (str): The name of the branch to checkout.
    
    Returns:
        str: The status of the checkout operation.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        try:
            repo.git.checkout(branch_name)
            return f"Checked out branch {branch_name}."
        except Exception as e:
            return f"Error checking out branch {branch_name}: {str(e)}"
    else:
        return f"Directory {local_dir} does not exist."
def create_branch(local_dir, branch_name):
    """
    Create a new branch in a local repository.
    
    Args:
        local_dir (str): The local directory of the repository.
        branch_name (str): The name of the new branch to create.
    
    Returns:
        str: The status of the branch creation operation.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        try:
            repo.git.checkout('-b', branch_name)
            return f"Created and checked out branch {branch_name}."
        except Exception as e:
            return f"Error creating branch {branch_name}: {str(e)}"
    else:
        return f"Directory {local_dir} does not exist."
def commit_changes(local_dir, commit_message, files=[]):
    """
    Commit changes in a local repository.
    
    Args:
        local_dir (str): The local directory of the repository.
        commit_message (str): The commit message.
    
    Returns:
        str: The status of the commit operation.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        try:
            if files:
                print('Adding files to commit ...')
                print(files)
                #need to remove ./ from file names as it is not recognized by git
                for file in files:
                    if file.startswith('./'):
                        file = file[2:]
                    print(f'Adding {file} to repo ...')
                    repo.index.add(file)
                #repo.index.add(files)
            
            repo.git.add(A=True)
            repo.git.commit(m=commit_message)
            return f"Committed changes with message: {commit_message}."
        except Exception as e:
            return f"Error committing changes: {str(e)}"
    else:
        return f"Directory {local_dir} does not exist."
def push_changes(local_dir, branch_name):
    """
    Push changes to a remote repository.
    
    Args:
        local_dir (str): The local directory of the repository.
        branch_name (str): The name of the branch to push.
    
    Returns:
        str: The status of the push operation.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        try:
            repo.git.push('origin', branch_name)
            return f"Pushed changes to branch {branch_name}."
        except Exception as e:
            print(f"Error pushing changes: {str(e)}")
            raise e
    else:
        return f"Directory {local_dir} does not exist."
def pull_changes(local_dir, branch_name):
    """
    Pull changes from a remote repository.
    
    Args:
        local_dir (str): The local directory of the repository.
        branch_name (str): The name of the branch to pull.
    
    Returns:
        str: The status of the pull operation.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        try:
            repo.git.pull('origin', branch_name)
            return f"Pulled changes from branch {branch_name}."
        except Exception as e:
            return f"Error pulling changes: {str(e)}"
    else:
        return f"Directory {local_dir} does not exist."
def fetch_changes(local_dir):
    """
    Fetch changes from a remote repository.
    
    Args:
        local_dir (str): The local directory of the repository.
    
    Returns:
        str: The status of the fetch operation.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        try:
            repo.git.fetch()
            return "Fetched changes from remote repository."
        except Exception as e:
            return f"Error fetching changes: {str(e)}"
    else:
        return f"Directory {local_dir} does not exist."
def stash_changes(local_dir):
    """
    Stash changes in a local repository.
    
    Args:
        local_dir (str): The local directory of the repository.
    
    Returns:
        str: The status of the stash operation.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        try:
            repo.git.stash()
            return "Stashed changes."
        except Exception as e:
            return f"Error stashing changes: {str(e)}"
    else:
        return f"Directory {local_dir} does not exist."
def apply_stash(local_dir):
    """
    Apply stashed changes in a local repository.
    
    Args:
        local_dir (str): The local directory of the repository.
    
    Returns:
        str: The status of the apply stash operation.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        try:
            repo.git.stash('apply')
            return "Applied stashed changes."
        except Exception as e:
            return f"Error applying stashed changes: {str(e)}"
    else:
        return f"Directory {local_dir} does not exist."
def reset_changes(local_dir):
    """
    Reset changes in a local repository.
    
    Args:
        local_dir (str): The local directory of the repository.
    
    Returns:
        str: The status of the reset operation.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        try:
            repo.git.reset('--hard')
            return "Reset changes."
        except Exception as e:
            return f"Error resetting changes: {str(e)}"
    else:
        return f"Directory {local_dir} does not exist."
def get_remote_url(local_dir):
    """
    Get the remote URL of a local repository.
    
    Args:
        local_dir (str): The local directory of the repository.
    
    Returns:
        str: The remote URL of the repository.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        remote_url = repo.remotes.origin.url
        return remote_url
    else:
        return f"Directory {local_dir} does not exist."
def set_remote_url(local_dir, new_url):
    """
    Set a new remote URL for a local repository.
    
    Args:
        local_dir (str): The local directory of the repository.
        new_url (str): The new remote URL to set.
    
    Returns:
        str: The status of the set remote URL operation.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        try:
            repo.remotes.origin.set_url(new_url)
            return f"Set new remote URL: {new_url}."
        except Exception as e:
            return f"Error setting remote URL: {str(e)}"
    else:
        return f"Directory {local_dir} does not exist."
def get_commit_history(local_dir, branch_name):
    """
    Get the commit history of a specific branch in a local repository.
    
    Args:
        local_dir (str): The local directory of the repository.
        branch_name (str): The name of the branch to get the commit history for.
    
    Returns:
        list: A list of commit messages.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        commits = list(repo.iter_commits(branch_name))
        commit_messages = [commit.message for commit in commits]
        return commit_messages
    else:
        return f"Directory {local_dir} does not exist."
def get_file_status(local_dir, file_path):
    """
    Get the status of a specific file in a local repository.
    
    Args:
        local_dir (str): The local directory of the repository.
        file_path (str): The path of the file to check the status for.
    
    Returns:
        str: The status of the file.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        try:
            status = repo.git.status(file_path)
            return status
        except Exception as e:
            return f"Error getting file status: {str(e)}"
    else:
        return f"Directory {local_dir} does not exist."
def get_diff(local_dir, file_path):
    """
    Get the diff of a specific file in a local repository.
    
    Args:
        local_dir (str): The local directory of the repository.
        file_path (str): The path of the file to get the diff for.
    
    Returns:
        str: The diff of the file.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        try:
            diff = repo.git.diff(file_path)
            return diff
        except Exception as e:
            return f"Error getting file diff: {str(e)}"
    else:
        return f"Directory {local_dir} does not exist."
def get_file_content(local_dir, file_path):
    """
    Get the content of a specific file in a local repository.
    
    Args:
        local_dir (str): The local directory of the repository.
        file_path (str): The path of the file to get the content for.
    
    Returns:
        str: The content of the file.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        try:
            with open(os.path.join(local_dir, file_path), 'r') as file:
                content = file.read()
            return content
        except Exception as e:
            return f"Error getting file content: {str(e)}"
    else:
        return f"Directory {local_dir} does not exist."
def add_files(local_dir, file_paths):
    """
    Add files to a local repository.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        try:
            #need to remove ./ from file names as it is not recognized by git
            for file_path in file_paths:
                if file_path.startswith('./'):
                    file_path = file_path[2:]
                print(f'Adding {file_path} to repo ...')
                repo.index.add(file_path)
                repo.git.add(file_path)
            repo.commit(m="Added files.")
            return f"Added file {file_path}."
        except Exception as e:
            return f"Error adding file: {str(e)}"
    else:
        return f"Directory {local_dir} does not exist."
def remove_file(local_dir, file_path):
    """
    Remove a file from a local repository.
    
    Args:
        local_dir (str): The local directory of the repository.
        file_path (str): The path of the file to remove.
    
    Returns:
        str: The status of the remove operation.
    """
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        try:
            repo.git.rm(file_path)
            return f"Removed file {file_path}."
        except Exception as e:
            return f"Error removing file: {str(e)}"
    else:
        return f"Directory {local_dir} does not exist."
def move_files(local_dir, src_file_paths, dest_file_paths):
    """
    Move files in a local repository to a new location.
    
    Args:
        local_dir (str): The local directory of the repository.
        src_file_paths (list): A list of source file paths to move.
        dest_file_paths (list): A list of destination file paths to move the files to.
    
    Returns:
        str: The status of the move operation.
    """
    print(f'Checking if directory {local_dir} exists ...')
    if os.path.exists(local_dir):
        repo = Repo(local_dir)
        print(f'Working directory for git mv cmd : {repo.git.working_dir}')
        #print(f'Checking if files exist ...')
        try:
            for src, dest in zip(src_file_paths, dest_file_paths):
                print(f'Moving {src} to {dest}')    
                repo.git.mv(src, dest)
            repo.index.add(dest_file_paths)
            # not adding commit here, as next step is commit in main program
            repo.git.commit(m="Moved files.")
            print('Moved files')
            return "Moved files."
                #os.rename(os.path.join(local_dir, src), os.path.join(local_dir, dest))
            return "Moved files."
        except Exception as e:
            print(f"Error moving files: {str(e)}")
            raise e
    else:
        print(f'Directory {local_dir} does not exist.')
        return f"Directory {local_dir} does not exist."