"""
Handle SSH private key
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from os import remove
from uuid import uuid4
from pykrete.args import CiIo
from .state import State
from .visitor import Visitor


class CiSshPrivateKey(Visitor):
    """Handle SSH private key specifid in the CI environment"""

    @property
    def is_enabled(self):
        """
        :return: True if the key is enabled, False otherwise
        """
        return self._state == State.Enabled

    def __init__(self, ci_io=None):
        self.__ci_io = ci_io if ci_io else CiIo()
        self._state = State.NotInitialized
        self._key_file = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.disable()

    def visit(self, target):
        """Visit this instance

        :param target: visited target
        """
        self._enable()
        target.set_ssh(self._key_file)

    def disable(self):
        """Disables the private key

        :exception: PermissionError - key already disabled
        """
        if self._must_not_be_disabled_but_is(State.NotInitialized):
            return
        remove(self._key_file)
        self._state = State.Disabled

    def _enable(self):
        if self._must_not_be_disabled_but_is(State.Enabled):
            return
        self._key_file = str(uuid4())
        key = self.__ci_io.read_env('deploy key')
        with open(self._key_file, 'w') as key_file:
            key_file.write(key)
        self._state = State.Enabled

    def _must_not_be_disabled_but_is(self, other_state):
        if self._state == State.Disabled:
            raise PermissionError('Credentials were disabled')
        return self._state == other_state
