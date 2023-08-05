"""
GIT repository push management
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import re
import git


class GitPush:
    """Handles pushing to a git repo"""
    __ssh_prefix = 'git@'

    def __init__(self, repo, credentials=None):
        """Initialize this repository

        :param repo: git repository
        :param credentials: git credential (optional, defaults to None)
        """
        self._repo = repo
        self._credentials = credentials
        self._credentials_set = self._credentials is None

    def push_to_origin(self, item):
        """Push the item to origin

        :param item: item to push
        """
        self._push_possibly_adding_credentials_and_trying_again_on_authentication_error(item)

    def _push_possibly_adding_credentials_and_trying_again_on_authentication_error(self, item):
        while True:
            try:
                self._repo.remotes.origin.push(item)
                break
            except git.GitCommandError as ex:
                if '403' not in ex.stderr:
                    raise
                self._set_credentials_once_for_this_instance()

    def _set_credentials_once_for_this_instance(self):
        if self._credentials_set:
            raise ConnectionRefusedError(
                f'Unable to connect with {"specified" if self._credentials else "no"} credentials'
                f' to {self._repo}')
        self._enable_credentials()

    def _enable_credentials(self):
        if not self._ssh_urls_configured_for_repo_origin():
            self._configure_ssh_url_for_repo_origin()
        self._credentials.enable()

    def _ssh_urls_configured_for_repo_origin(self):
        return [url for url in
                self._repo.remotes.origin.urls if url.startswith(self.__ssh_prefix)]

    def _configure_ssh_url_for_repo_origin(self):
        http_url, server, project = self._get_http_url_server_and_project()
        ssh_url = self._make_ssh_url(server, project)
        self._repo.remotes.origin.set_url(ssh_url, http_url)

    def _get_http_url_server_and_project(self):
        pattern = re.compile(r'http.?://([^/]+)/(.*)')
        matches = [match for match in
                   [(url, pattern.match(url)) for url in self._repo.remotes.origin.urls]
                   if match[1]]
        if not matches:
            raise IOError('No HTTP* URLs found in repo.origin')
        first_match = matches[0]
        return (first_match[0], ) + tuple(first_match[1].groups())

    @staticmethod
    def _make_ssh_url(server, project):
        return f'{GitPush.__ssh_prefix}{server}:{project}'
