"""
Pykrete repo.Git tests
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""

import unittest
import logging
import uuid
from git import GitCommandError
from pykrete.repo import Git
from pykrete.tests.helpers import get_full_path


class PythonGitEndToEndTestCase(unittest.TestCase):
    """E2E tests for pykrete's repo module's Git class
    """

    _logger = logging.getLogger(__name__)

    def test_get_all_tags(self):
        """Verifies getting all tags from repo
        """
        self._assert_get_tags(lambda git: git.get_all_tags(),
                              ('1.0.0', None), ('1.0.1', 'bug fix'))

    def test_get_tags_from_existing(self):
        """Verifies getting all tags from repo starting from a specific tag
        """
        self._assert_get_tags(lambda git: git.get_tags_from(r'.*?0\.1', True),
                              ('1.0.1', 'bug fix'))

    def test_get_tags_from_must_but_non_existing(self):
        """Verifies getting all tags from repo
        """
        with self.assertRaises(KeyError):
            self._assert_get_tags(lambda git: git.get_tags_from(r'no such tag', True))

    def test_get_tags_from_non_must_non_existing(self):
        """Verifies getting all tags from repo
        """
        self._assert_get_tags(lambda git: git.get_tags_from(r'no such tag', False),
                              None, ('1.0.0', None), ('1.0.1', 'bug fix'))

    def test_get_head_change(self):
        """Verifies a non-empty head-change returned from repo"""
        target = self._make_target()
        change = target.get_head_change()
        self.assertIsNotNone(change, 'empty change returned')
        self._logger.debug(change)
        self.assertIsNotNone(change.log, 'empty log returned')
        self.assertIsNotNone(change.details, 'empty log returned')

    def test_add_remove_tag_fails_with_no_credentials(self):
        """Verifies adding and removing tag in the repo"""
        target = self._make_target(get_full_path('testing-grounds', True))
        expected = (str(uuid.uuid4()), 'test add remove tag')
        with self.assertRaises(GitCommandError):
            new_tag = target.add_tag(expected[0], expected[1])
            self.assertEqual(expected, new_tag, 'new tag not as expected')
            self.assertTrue(expected in target.get_all_tags(), 'new tag not found')
            target.remove_tag(expected[0])
            self.assertFalse(expected in target.get_all_tags(), 'removed tag still found')

    def test_remove_non_existing_tag(self):
        """Verifies adding and removing tag in the repo"""
        target = self._make_target(get_full_path('testing-grounds', True))
        with self.assertRaises(KeyError):
            target.remove_tag(str(uuid.uuid4()))

    def _assert_get_tags(self, getter, *expected):
        """Verifies tags from repo

        :param getter: tag getter (lambda on Git object)
        :param expected: expected returned tags
        :return:
        """
        target = self._make_target()
        tags = getter(target)
        self._logger.debug(tags)
        self.assertTrue(tags, 'Got empty tags')
        self.assertTrue(len(tags) >= len(expected), 'too few tags returned')
        for test in zip(expected, tags):
            self.assertEqual(test[0], test[1], 'wrong tag returned')

    @staticmethod
    def _make_target(path=None):
        test_repo_path = path if path else get_full_path('git-tag-example', True)
        return Git(test_repo_path)


if __name__ == '__main__':
    unittest.main()
