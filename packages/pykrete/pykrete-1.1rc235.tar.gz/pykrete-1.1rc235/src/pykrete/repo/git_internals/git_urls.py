"""
GIT repository URL management
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import re


class GitUrls:
    """Handles the URLs attached to a remote"""

    __ssh_prefix = 'git@'

    @property
    def configured_ssh_urls(self):
        """
        :return SSH urls configured for this remote
        """
        return [url for url in
                self._remote.urls if url.startswith(self.__ssh_prefix)]

    def __init__(self, remote):
        """Initialize this repository

        :param remote: git remote
        """
        self._remote = remote

    def configure_ssh_url_and_save_original(self):
        """Configures an SSH url instead of existing HTTP url

        :return: (original, new) URLs
        """
        http_url, server, project = self._get_http_url_server_and_project_for_remote()
        ssh_url = self._make_ssh_url(server, project)
        self.replace_url(ssh_url, http_url)
        return http_url, ssh_url

    def replace_url(self, new, old):
        """Replace remote URL

        :param new: new URL to use
        :param old: olf URL to replace
        """
        self._remote.set_url(new, old)

    def _get_http_url_server_and_project_for_remote(self):
        pattern = re.compile(r'http.?://([^/]+)/(.*)')
        matches = [match for match in
                   [(url, pattern.match(url)) for url in self._remote.urls]
                   if match[1]]
        if not matches:
            raise IOError(f'No HTTP* URLs found in {self._remote}')
        first_match = matches[0]
        return (first_match[0], ) + tuple(first_match[1].groups())

    @staticmethod
    def _make_ssh_url(server, project):
        return f'{GitUrls.__ssh_prefix}{server}:{project}'
