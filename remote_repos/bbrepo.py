'''
Operations related to Bitbucket repositories.
This module provides functions to create, delete, and manage Bitbucket repositories.
It also includes functions to check the status of a repository and to get the list of repositories.
It uses the Bitbucket API to perform these operations.
It is assumed that the user has already authenticated with Bitbucket and has the necessary permissions to perform these operations.
'''
import os
from atlassian import Bitbucket

def get_instance():
    """
    Get a Bitbucket instance.
    :return: Bitbucket instance
    """
    try:
        bitbucket = Bitbucket(
            url=os.getenv('BITBUCKET_URL'),
            username=os.getenv('BITBUCKET_USERNAME'),
            password=os.getenv('BITBUCKET_PASSWORD')
        )
        return bitbucket
    except Exception as e:
        print(f"Error creating Bitbucket instance: {e}")
        return None

def get_repo(bitbucket, repo_slug):
    """
    Get the status of a Bitbucket repository.
    :param bitbucket: Bitbucket instance
    :param repo_slug: Repository slug
    :return: Repository status
    """
    try:
        repo = bitbucket.get_repo(repo_slug)
        return repo
    except Exception as e:
        print(f"Error getting repository status: {e}")
        return None
    return None

def create_branch(bitbucket, repo_slug, branch_name, base_branch):
    """
    Create a new branch in a Bitbucket repository.
    :param bitbucket: Bitbucket instance
    :param repo_slug: Repository slug
    :param branch_name: Name of the new branch
    :param base_branch: Base branch to create the new branch from
    :return: branch object or None
    """
    try:
        branch = bitbucket.create_branch(repo_slug, branch_name, base_branch)
        print(f"Branch '{branch_name}' created successfully from '{base_branch}'")
        return branch
    except Exception as e:
        print(f"Error creating branch: {e}")
        return None
    return None
def delete_branch(bitbucket, repo_slug, branch_name):
    """
    Delete a branch in a Bitbucket repository.
    :param bitbucket: Bitbucket instance
    :param repo_slug: Repository slug
    :param branch_name: Name of the branch to delete
    :return: None
    """
    try:
        bitbucket.delete_branch(repo_slug, branch_name)
        print(f"Branch '{branch_name}' deleted successfully")
    except Exception as e:
        print(f"Error deleting branch: {e}")
        return None
    return None
def get_repos(bitbucket, project_key):
    """
    Get the list of repositories in Bitbucket.
    :param bitbucket: Bitbucket instance
    :param project_key: Project key
    :return: List of repositories
    """
    try:
        repos = bitbucket.repo_list(project_key)
        return repos
    except Exception as e:
        print(f"Error getting repositories: {e}")
        return None
    return None
def open_pull_request(bitbucket, project, repo_slug, source_branch, target_branch, title, description):
    """
    Open a pull request in Bitbucket.
    :param bitbucket: Bitbucket instance
    :param project: Project key
    :param repo_slug: Repository slug
    :param source_branch: Source branch for the pull request
    :param target_branch: Target branch for the pull request
    :param title: Title of the pull request
    :param description: Description of the pull request
    :return: pull request object or None
    """
    try:
        pr = bitbucket.open_pull_request(source_project=project,
                                    source_repo=repo_slug,
                                    dest_project=project,
                                    dest_repo=repo_slug,
                                    source_branch=source_branch,
                                    destination_branch=target_branch, 
                                    title=title, description=description)
        print(f"Pull request '{title}' crceated successfully from '{source_branch}' to '{target_branch}'")
        return pr
    except Exception as e:
        print(f"Error creating pull request: {e}")
        return None
    return None