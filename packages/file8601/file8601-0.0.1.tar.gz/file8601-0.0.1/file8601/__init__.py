"""
file8601
    Copyright (C) 2020  Brian Pond (brian@pondconsulting.net)

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

# Standard Python library packages
import datetime
import logging
from glob import glob
from operator import itemgetter
import os
import pathlib
import pprint  # Python's pretty-print library
import re

# PyPI
import dateutil.parser
from dateutil import tz

# Global variables
__version__ = "0.0.1"  # Setuptools reads this during package installation.
__version_info__ = tuple(map(int, __version__.split('.')))

# Configure Python logging
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


# Instances methods
def getPackageVersion():
	return __version__


class StampFilename():
	""" Class to stamp files with datetimes """
	def validate_parameters(_file_name, _parmDateTime):
		if not (isinstance(_file_name, str) or isinstance(_file_name, pathlib.Path.__base__)):
			logger.error(f"  Parameter 'file_name' is of type: {type(_file_name)}")
			raise TypeError("Function 'add_suffix' expects parameter 'file_name' to be of type String or pathlib.Path")
		if _parmDateTime and not isinstance(_parmDateTime, datetime.datetime.__base__):
			logger.error(f"  Parameter 'file_datetime' is of type: {type(_parmDateTime)}")
			raise TypeError("Function 'add_suffix' expects parameter 'file_datetime' to be of type DateTime")
		if _parmDateTime and _parmDateTime.tzinfo is None:
			raise ValueError("When passing datetime parameter, time zone information must be included.")

	def __init__(self, file_name, parmDateTime=None):
		# Validate parameters, before assigning to class variables.
		StampFilename.validate_parameters(file_name, parmDateTime)
		self.filename_orig = file_name
		self.file_path = pathlib.Path(file_name)
		# If not provided, set datetime to current local datetime, with local tzinfo.
		self.datetime = parmDateTime or datetime.datetime.now().astimezone().replace(microsecond=0)
		self.datetime_iso = self.datetime.isoformat().replace(':', '')

	def add_prefix(self):
		""" Given a filename (string or Path), return the filename with an ISO 8601 string prefixed."""
		new_name = self.datetime_iso + '_' + self.file_path.name
		print(new_name)
		return self._format_result(new_name)

	def add_suffix(self):
		""" Given a filename (string or Path), return the filename with a datetime value appended."""
		# Fanciness to properly split file names into 2 parts:
		digits = ('.1', '.2', '.3', '.4', '.5', '.6', '.7', '.8', '.9', '.0')
		failsafe = 0
		filename_tail = ''
		filename_head = pathlib.Path(self.file_path.name)
		while failsafe < 10:  # no more than 10 attemps to split
			if not filename_head.suffix:
				break  # no more suffixes
			if(filename_head.suffix.startswith(digits)):
				break  # found a leading digit
			filename_tail = filename_head.suffix + filename_tail
			filename_head = pathlib.Path(filename_head.stem)
			failsafe += 1

		# Build the new filename
		new_filename = str(filename_head) + '_' + self.datetime_iso + filename_tail
		return self._format_result(new_filename)

	def _format_result(self, new_filename):
		# Return the same datatype as was originally passed to Class.
		if isinstance(self.filename_orig, str):
			return new_filename   # return a String to caller
		else:
			return self.filename_orig.parent / new_filename   # return a Path to caller


class Directory():
	def __init__(self, directory_path):
		self._validate_parameters(directory_path)
		self.directory_path = pathlib.Path(directory_path)

	def _validate_parameters(self, _path):
		if not isinstance(_path, pathlib.Path.__base__):
			_path = pathlib.Path(_path)
		if not _path.exists():
			raise FileNotFoundError(f"Directory at path '{_path}' does not exist.")
		if _path.exists() and _path.is_file():
			raise TypeError(f"Expected path to Directory, but found path to File: '{_path}'.")

	def build_directory_metadata(self, glob_tuple=None, pretty_print=False):
		"""Given a directory path to files, creates a dictionary of metadata"""
		if glob_tuple and not isinstance(glob_tuple, tuple):
			raise ValueError("Value passed in parameter 'glob_tuple' is not a Python Tuple.")

		result = {}
		result['directory'] = self.directory_path
		result['files'] = []

		if not glob_tuple:
			files = self.directory_path.iterdir()
		else:
			files = []
			for criteria in glob_tuple:
				search_string = str(self.directory_path / criteria)
				files.extend(glob(search_string))

		for file_path in files:
			try:
				file_dict = build_file_metadata(file_path)
			except ValueError:
				logger.warning(f"Skipping file; does not have valid ISO 8601 name: {file_path}")
				continue  # if file not valid, quietely skip to next file in directory.
			result['files'].append(file_dict)

		if pretty_print:
			pprint_instance = pprint.PrettyPrinter(indent=4)
			print(f"\n{pprint_instance.pprint(result)}\n")

		return result


def get_datetime_pattern():
	"""Returns an ISO 8601 datetime pattern, for use with regular expressions."""
	pattern = ''
	pattern += "([0-9]{4})"  # year
	pattern += "-?(1[0-2]|0[1-9])"  # month
	pattern += "-?(3[01]|0[1-9]|[12][0-9])"  # day
	pattern += "T"
	pattern += "(2[0-3]|[01][0-9])"  # hour
	pattern += ":?([0-5][0-9])"  # minute
	pattern += ":?([0-5][0-9])"  # second
	pattern += "-?(2[0-3]|[01][0-9])"  # offset hour
	pattern += ":?([0-5][0-9])"  # offset minute
	return pattern


def validate_datetime_string(datetime_string):
	"""Verify that a string is a valid ISO 8601 datetime"""
	# Returns: True or False
	pattern = '^' + get_datetime_pattern() + '$'  # start to finish, string must be a complete datetime
	re_object = re.compile(pattern)  # Regular Expression Object
	return re_object.match(datetime_string)


def parse_file_path(anypath):
	"""Given any string, parse and return a tuple of prefix, ISO 8601 string, suffix"""
	# Returns: tuple
	if isinstance(anypath, pathlib.Path.__base__):
		name_string = anypath.name
	else:
		name_string = str(anypath)
	
	match_object = re.search(get_datetime_pattern(), name_string)
	if not match_object:
		raise ValueError(f"Could not find an ISO 8601 pattern in path '{anypath}'")

	# logger.debug(f"String Index Start: {match_object.span()[0]}, String Index End: {match_object.span()[1]}")

	prefix = name_string[:match_object.start() - 1]
	datetime_string = name_string[match_object.start():match_object.end()]
	suffix = name_string[match_object.end():]  # includes the leading period (.)

	if not validate_datetime_string(datetime_string):
		logger.error(f"String: {name_string}")
		logger.error(f"Indices: {match_object.span()}")
		logger.error(f"Datetime String: {datetime_string}")
		raise Exception("Unhandled exception. Regular expression object has indices for datetime string, but string validation.")
	
	ret = (prefix, datetime_string, suffix)
	# logger.debug(f"Tuple: {ret}")
	return ret


def validate_file_path(_path, must_exist=False):
	"""Validate a file path meets required syntax"""

	if not isinstance(_path, pathlib.Path.__base__):
		_path = pathlib.Path(_path)

	if must_exist and not _path.exists():
		raise FileNotFoundError(f"File with path '{_path}' does not exist.")
	
	if _path.exists() and _path.is_dir():
		raise TypeError(f"Expected path to File, but found path to Directory: '{_path}'.")

	# Use regex to validate the datetime string
	match_object = re.search(get_datetime_pattern(), _path.name)
	if not match_object:
		raise ValueError(f"Could not find an ISO 8601 pattern in file: '{_path.name}'")

	return _path


def build_file_metadata(file_path, file_must_exist=False):
	"""Creates a dictionary of a file's datetime attributes"""
	
	file_path = validate_file_path(file_path, file_must_exist)
	parse_results = parse_file_path(file_path)
	file_datetime = dateutil.parser.parse(parse_results[1])
	timezone_utc = tz.gettz('UTC')
	datetime_utc = file_datetime.astimezone(timezone_utc)

	# Create a dictionary of path metadata
	file_dict = {}
	file_dict['path'] = file_path
	file_dict['parentdir'] = str(file_path.parent.resolve())
	file_dict['full_name'] = file_path.name
	file_dict['prefix'] = parse_results[0]  # no datetime, no suffix/extension
	file_dict['datetime_string'] = parse_results[1]
	file_dict['suffix'] = parse_results[2]
	file_dict['orig_datetime'] = file_datetime
	file_dict['utc_datetime'] = datetime_utc
	file_dict['utc_date'] = datetime_utc.date()
	file_dict['utc_time'] = datetime_utc.time()
	
	return file_dict


def add_sortcodes(directory_metadata):
	"""Given either a dict or array of metadata, add the Sort Keys"""
	if isinstance(directory_metadata, list):
		parameter_type = 'List'
		working_array = directory_metadata
	elif isinstance(directory_metadata, dict) and "directory" in directory_metadata.keys() and \
	     "files" in directory_metadata.keys():
		# Received a Dict, but need to work with a List.
		parameter_type = 'Dict'
		working_array = directory_metadata['files']
	else:
		raise TypeError(f"Function called with invalid parameter. Type = {type(directory_metadata)}")

	# Sorted in total, by UTC DateTime
	last_date = None
	day_index = None
	unique_day_index = -1
	working_array = sorted(working_array, key=itemgetter('utc_datetime'), reverse=True)
	for index, filedict in enumerate(working_array):
		working_array[index]['newness_in_list'] = index

		# For each UTC day, assign a sortcode within that day.
		# Allows you to fetch last file of day, first file of day, Nth file of day
		if not last_date or (last_date != working_array[index]['utc_date']):
			last_date = working_array[index]['utc_date']
			day_index = 0
			working_array[index]['newness_in_day'] = day_index
			unique_day_index += 1
			working_array[index]['date_occurence'] = unique_day_index
		else:
			day_index += 1
			working_array[index]['newness_in_day'] = day_index
			working_array[index]['date_occurence'] = unique_day_index

	# Return the same Python Type we were passed.
	if parameter_type == 'Dict':
		return_dict = {}
		return_dict['directory'] = directory_metadata['directory']
		return_dict['files'] = working_array
		return return_dict
	else:
		return working_array
