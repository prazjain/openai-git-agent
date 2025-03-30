from remote_repos.remote_repo_facade import RemoteRepoFacade
from remote_repos import githubrepo

class GithubRepoFacade(RemoteRepoFacade):
    """
    Facade for managing Github repositories.
    """

    def __init__(self, repo_name):
        """
        Initialize the GithubFacade with a Github repository.

        :param repo: The Github repository to manage.
        """

        self.github = githubrepo.get_instance()
        self.repo = githubrepo.get_repo(self.github, repo_name=repo_name)
        super().__init__(repo_name)
    
    def get_repo(self):
        """
        Get the repository.

        :return: The repository from subclass.
        """
        return self.repo
    def get_branch(self, branch_name):
        """
        Get the branch.
        :param branch_name: The name of the branch.
        :return: The branch from subclass.
        """
        if self.repo:
            return self.repo.get_branch(branch_name)
        return None
    def create_pull_request(self, title, body, head, base):
        """
        Create a pull request.
        :param title: The title of the pull request.
        :param body: The body of the pull request.
        :param head: The head branch of the pull request.
        :param base: The base branch of the pull request.
        :return: The pull request object.
        """
        pr = self.repo.create_pull(
            title=title,
            body=body,
            head=head,
            base=base,
        )
        return pr.html_url
    