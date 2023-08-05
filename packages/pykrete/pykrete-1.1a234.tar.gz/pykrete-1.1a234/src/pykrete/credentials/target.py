"""
Security credentials target
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from abc import abstractmethod


class Target:
    """Visitor pattern - base class for credentail targets
    """
    def accept(self, visitor):
        """Accept a visitor

        :param visitor: visitor
        :type visitor: class implementing 'visit'
        """
        return visitor.visit(self)

    @abstractmethod
    def set_ssh(self, private_key_file_path):
        """Set the SSH credentials from the supplied file

        :param private_key_file_path: path to private key file
        :type private_key_file_path: string
        """
