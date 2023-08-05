"""
GIT repository management
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
import git
from pykrete.repo.change import Change
from pykrete.repo.repo import Repo
from .git_internals.git_push import GitPush
from .git_internals.git_tags import GitTagsReader


class Git(Repo):
    """Handles a GIT repository"""

    def __init__(self, path='.', credentials=None):
        """Initialize this repository

        :param path: path to repository (optional, defaults to the CWD)
        :param credentials: git credential (optional, defaults to None)
        """
        self._logger = logging.getLogger(__name__)
        self._repo = git.Repo.init(path)
        self._credentials = credentials
        self._tag_reader = GitTagsReader(self._repo)

    def add_tag(self, name, message):
        """Adds a tag to the repo

        :param name: tag name
        :param message: tag message
        :return: the new tag's info tuple (name, message)
        """
        new_tag = self._repo.create_tag(name, message=message)
        self._push_origin([new_tag])
        return self._tag_reader.name_message_tuple_from_tag_ref(new_tag)

    def remove_tag(self, name, is_must=True):
        """Adds a tag to the repo

        :param name: tag name
        :param is_must: True to raise an error tag doesn't exist, False to just skip in that case.
        :exception: KeyError - tag not found
        """
        old_tags = self._tag_reader.get_last_tag_named(name, is_must)
        old_tag = old_tags[0]
        self._repo.delete_tag(old_tags)
        self._push_origin([old_tag])

    def get_all_tags(self):
        """Gets all tags from the current branch in the repo

        :return: A list of tag info tuples (name, message)
        """
        return GitTagsReader(self._repo).tags

    def get_tags_from(self, pattern, is_must=False):
        """Gets all tags from the current branch in the repo, from the tag whose name matches the
         supplied pattern.

        :param pattern: name pattern to match
        :param is_must: True to raise an error if no match is found, False to return all tags in
        that case (with the first tuple as None).
        :return: A list of tag info tuples (name, message)
        :exception: KeyError - tag not found
        """
        return self._tag_reader.get_tags_from(pattern, is_must)

    def get_head_change(self, branch=None):
        """Gets the last change in the branch

        :param branch: branch name (optional, defaults to the current branch)
        :return: (pykrete.repo.Change) last change in the branch
        """
        commit = self._repo.commit(branch)
        return self.__append_commits_to_change([commit])

    def _push_origin(self, items):
        with GitPush(self._repo, self._credentials) as pusher:
            for item in items:
                pusher.push(item)

    @staticmethod
    def __append_commits_to_change(commits, change=Change()):
        for commit in commits:
            if commit:
                if commit.summary:
                    change.append_log(commit.summary)
                if commit.message:
                    change.append_details(commit.message)
        return change
