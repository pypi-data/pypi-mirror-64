"""
CI environment-based version information manager
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from pykrete.args import CiIo
from .version import Version
from .ci_revision import CiRevision


class CiVersion(Version):
    """Handle version in CI environment
    Version parts are read from CI variables CI_VERSION_MAJOR, CI_VERSION_MINOR and CI_PIPELINE_IID
    Revision is read from CI_COMMIT_REF_NAME, CI_MERGE_REQUEST_TITLE and CI_JOB_NAME:
        Release - in master branch and job's name doesn't contain '_rc_'
        RC - in non-WIP merge request, or in master branch with a job who'se name contains '_rc_'
        Beta - in merge request with 'WIP' in the title
        Alpha - none of the above
    """
    def __init__(self, ci_io=None):
        """Initializes this instance from CI environment

        :param ci_io: CI environment's IO manager (optional, defaults to pykrete.args.CiIo)
        """
        self.__ci_io = ci_io if ci_io else CiIo()
        revision_type = CiRevision(self.__ci_io).revision_type
        super().__init__(major=self.__ci_io.read_env('major version'),
                         minor=self.__ci_io.read_env('minor version'),
                         revision=revision_type.value,
                         build=self.__ci_io.read_env('build version'),
                         revision_type=revision_type)
