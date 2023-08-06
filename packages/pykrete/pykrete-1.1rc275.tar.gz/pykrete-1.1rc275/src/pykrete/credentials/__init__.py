"""
Security credentials management
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from .target import Target
from .ci_ssh_private_key import CiSshPrivateKey

__all__ = ['Target', 'CiSshPrivateKey']
