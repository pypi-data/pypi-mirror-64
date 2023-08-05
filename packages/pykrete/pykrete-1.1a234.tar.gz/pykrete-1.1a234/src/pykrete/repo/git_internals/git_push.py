"""
GIT repository push management
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from pykrete.credentials import Target
from .git_urls import GitUrls
from .git_ssh import GitSsh


class GitPush(Target):
    """Handles pushing to a git repo"""

    __ssh_prefix = 'git@'

    def __init__(self, repo, credentials=None, remote='origin'):
        """Initialize this repository

        :param repo: git repository
        :param credentials: git credential (optional, defaults to None)
        """
        self._repo = repo
        self._credentials = credentials
        self._remote = repo.remotes[remote]
        self._urls = GitUrls(self._remote)
        self._active_credentials = None

    def __enter__(self):
        if self._credentials:
            self.accept(self._credentials)
        return self

    def __exit__(self, *args):
        if self._active_credentials:
            self._active_credentials.unset(*args)

    def push(self, item):
        """Push the item

        :param item: item to push
        """
        self._remote.push(item)

    def set_ssh(self, private_key_file_path):
        """Set SSH private key to the specified path

        :param private_key_file_path: Path to private key file
        """
        self._active_credentials = GitSsh(
            self._repo.git.custom_environment, self._urls, private_key_file_path)
