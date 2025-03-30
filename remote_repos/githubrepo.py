'''
Operations related to Github repositories.
This module provides functions to create, delete, and manage Github repositories.
It also includes functions to check the status of a repository and to get the list of repositories.
It uses the Github API to perform these operations.
It is assumed that the user has already authenticated with Github and has the necessary permissions to perform these operations.
'''
from github import Github
import os
import logging 
import logging_config

logger = logging.getLogger(__name__)

def get_instance():
    """
    Get a Github instance.
    :return: Github instance
    """
    try:
        github = Github(
            login_or_token=os.getenv('GITHUB_TOKEN')
        )
        return github
    except Exception as e:
        logger.error(f"Error creating Github instance: {e}")
        return None
def get_repo(github, repo_name):
    """
    Get a Github repository.
    :param github: Github instance
    :param repo_name: Repository name
    :return: Repository status
    """
    try:
        repo = github.get_repo(repo_name)
        return repo
    except Exception as e:
        logger.error(f"Error getting repository status: {e}")
        return None
    return None
def create_branch(github, repo_name, branch_name, base_branch):
    """
    Create a new branch in a Github repository.
    :param github: Github instance
    :param repo_name: Repository name
    :param branch_name: Name of the new branch
    :param base_branch: Base branch to create the new branch from
    :return: None
    """
    try:
        repo = github.get_repo(repo_name)
        base = repo.get_branch(base_branch)
        repo.create_git_ref(ref='refs/heads/' + branch_name, sha=base.commit.sha)
        logger.info(f"Branch '{branch_name}' created successfully from '{base_branch}'")
    except Exception as e:
        logger.error(f"Error creating branch: {e}")
        return None
    return None
def delete_branch(github, repo_name, branch_name):
    """
    Delete a branch in a Github repository.
    :param github: Github instance
    :param repo_name: Repository name
    :param branch_name: Name of the branch to delete
    :return: None
    """
    try:
        repo = github.get_repo(repo_name)
        ref = repo.get_git_ref('heads/' + branch_name)
        ref.delete()
        logger.info(f"Branch '{branch_name}' deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting branch: {e}")
        return None
    return None
def get_repos(github):
    """
    Get the list of repositories for the authenticated user.
    :param github: Github instance
    :return: List of repositories
    """ 
    try:
        repos = github.get_user().get_repos()
        return repos
    except Exception as e:
        logger.error(f"Error getting repositories: {e}")
        return None
    return None
def create_pull_request(github, repo_name, title, body, head, base):
    """
    Create a pull request in a Github repository.
    :param github: Github instance
    :param repo_name: Repository name
    :param title: Title of the pull request
    :param body: Body of the pull request
    :param head: Head branch for the pull request
    :param base: Base branch for the pull request
    :return: Pull request object
    """
    try:
        repo = github.get_repo(repo_name)
        pr = repo.create_pull(title=title, body=body, head=head, base=base)
        return pr
    except Exception as e:
        logger.error(f"Error creating pull request: {e}")
        return None
