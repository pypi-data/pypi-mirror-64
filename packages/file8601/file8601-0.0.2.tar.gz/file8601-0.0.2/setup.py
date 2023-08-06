# https://setuptools.readthedocs.io/en/latest/setuptools.html#developer-s-guide

import ast
from os import geteuid as os_geteuid
import pathlib
import platform
import re
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
import sys

# globals
_PACKAGENAME = 'file8601'
_MIN_PYTHON_VERSION = (3, 7, 0)  # Python 3.7.0 was released June 2018
_REQUIRES_PATH = 'package_reqs/install_requires.txt'


def getPackageVersion():
	''' # Retrieve the Package version from __version__ variable in _PACKAGENAME/__init__.py '''
	''' # https://packaging.python.org/guides/single-sourcing-package-version/ '''
	version_pattern = re.compile(r'__version__\s+=\s+(.*)')
	path_to_init = pathlib.Path(_PACKAGENAME) / '__init__.py'
	with open(path_to_init, 'rb') as f:
		app_version = str(ast.literal_eval(version_pattern.search(
			f.read().decode('utf-8')).group(1)))
	if not app_version:
		raise ValueError(f"Unable to find variable '__version__' in file {path_to_init}")
	return app_version


def makeInstallRequires():
	with open(_REQUIRES_PATH) as f:
		return f.read().strip().split('\n')


def makePythonRequires():
	''' Workaround because of this issue: https://github.com/pypa/setuptools/issues/1633 '''
	''' python_requires refers to the version of the -installed- package. Not the version of the build system.'''
	''' I want to validate both, so I wrote this short function. '''
	assert (sys.version_info >= _MIN_PYTHON_VERSION), \
	       "Minimum Python version is {}".format('.'.join(str(v) for v in _MIN_PYTHON_VERSION))
	return (">= " + platform.python_version())


def preInstallSequence(_setupToolsMode):
	# Do not install package as root
	if os_geteuid() == 0:
		raise Exception("Install should be as a non-privileged user")


def postInstallSequence(_setupToolsMode):
    pass


class InstallOverride(install):
	"""Additional work when running in Install mode."""
	''' https://www.anomaly.net.au/blog/running-pre-and-post-install-jobs-for-your-python-packages/ '''
	def run(self):
		preInstallSequence('install')
		install.run(self)
		postInstallSequence('install')


class DevelopOverride(develop):
	"""Additional work when running in Develop mode."""
	''' https://www.anomaly.net.au/blog/running-pre-and-post-install-jobs-for-your-python-packages/ '''
	def run(self):
		preInstallSequence('develop')
		develop.run(self)
		postInstallSequence('develop')


setup(
	name=_PACKAGENAME,  # The name pip will refer to.
	version=getPackageVersion(),
	packages=find_packages(),
	python_requires=makePythonRequires(),
	install_requires=makeInstallRequires(),
	include_package_data=False,
	# metadata to display on PyPI
	author='Brian Pond',
	author_email='brian@pondconsulting.net',
	description='A library for working with ISO 8601 in file names.',
    long_description='Adds ISO 8601 datetime to file names as a suffix.\
Given a list/directory of such files, generates useful metadata about the files.  Including sort codes, for determining the chronological order of files in the directory(s)',
	keywords="datetime",
	license="MIT",
	platforms=["Linux"],
	url="https://gitlab.com/brian_pond/file8601",
	zip_safe=False,
	# Additional code to run Before & After installation.
	cmdclass={'install': InstallOverride,
	          'develop': DevelopOverride}
)
