"""
Pykrete module build script
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from setuptools import setup

__version__ = '0.99.99'
exec(open('./src/pykrete/version.py').read())
print('Installing pykrete v.' + __version__)
with open('./requirements.txt') as f:
    REQUIREMENTS = f.read().splitlines()
with open('./README.md') as f:
    LONG_DESCRIPTION = f.read()
setup(
    name='pykrete',
    version=__version__,
    license='MIT',
    author='Shai A. Bennathan',
    author_email='shai.bennathan@intel.com',
    description='Build script foundation',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='http://ait-tool-center.iil.intel.com/',
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=REQUIREMENTS
)
