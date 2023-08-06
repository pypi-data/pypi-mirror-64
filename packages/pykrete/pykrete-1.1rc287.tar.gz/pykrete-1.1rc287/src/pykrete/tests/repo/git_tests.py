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
from pykrete.credentials import CiSshPrivateKey


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
        self._assert_change_not_empty(change)

    def test_add_tag_fails_with_no_credentials(self):
        """Verifies adding and removing tag in the repo"""
        target = self._make_testing_ground_target(None)
        with self.assertRaises(GitCommandError):
            try:
                name = str(uuid.uuid4())
                target.add_tag(name, 'test add remove tag failure')
            finally:
                target.remove_tag(name)

    def test_add_remove_tag_with_ssh_credentials(self):
        """Verifies adding and removing tag in the repo"""
        with CiSshPrivateKey() as key:
            try:
                expected, target = self._make_target_and_expected_token(key)
                self._test_add_tag(expected, target)
            finally:
                self._test_remove_tag(expected, target)

    def _assert_change_not_empty(self, change):
        self.assertIsNotNone(change, 'empty change returned')
        self._logger.debug(change)
        self.assertIsNotNone(change.log, 'empty log returned')
        self.assertIsNotNone(change.details, 'empty log returned')

    def _test_add_tag(self, expected, target):
        new_tag = target.add_tag(expected[0], expected[1])
        target.add_tag(expected[0] + 'remain', expected[1] + 'remain')
        self.assertEqual(expected, new_tag, 'new tag not as expected')
        self.assertTrue(expected in target.get_all_tags(), 'new tag not found')
        return expected, target

    def _make_target_and_expected_token(self, key):
        target = self._make_testing_ground_target(key)
        expected = (str(uuid.uuid4()), 'test add remove tag')
        return expected, target

    def _test_remove_tag(self, expected, target):
        target.remove_tag(expected[0])
        self.assertFalse(expected in target.get_all_tags(), 'removed tag still found')

    def test_remove_non_existing_tag(self):
        """Verifies adding and removing tag in the repo"""
        target = self._make_testing_ground_target(None)
        with self.assertRaises(KeyError):
            target.remove_tag(str(uuid.uuid4()))

    def _assert_get_tags(self, getter, *expected):
        """Verifies tags from repo

        :param getter: tag getter (lambda on Git object)
        :param expected: expected returned tags
        :return:
        """
        tags = self._make_tags(getter)
        self._assert_tags(expected, tags)

    def _make_tags(self, getter):
        target = self._make_target()
        tags = getter(target)
        self._logger.debug(tags)
        return tags

    def _assert_tags(self, expected, tags):
        self.assertTrue(tags, 'Got empty tags')
        self.assertTrue(len(tags) >= len(expected), 'too few tags returned')
        for test in zip(expected, tags):
            self.assertEqual(test[0], test[1], 'wrong tag returned')

    @staticmethod
    def _make_testing_ground_target(credentials):
        return Git(get_full_path('testing-grounds', True), credentials)

    @staticmethod
    def _make_target(path=None, credentials=None):
        test_repo_path = path if path else get_full_path('git-tag-example', True)
        return Git(test_repo_path, credentials)


if __name__ == '__main__':
    unittest.main()
