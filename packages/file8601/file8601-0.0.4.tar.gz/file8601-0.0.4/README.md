# File8601

This package provides 3 key functions:

1. Given a filename, intelligently embed a valid ISO 8601 datetime string into the name.  Storing datetime in filenames is useful in many applications, such as backup scripts.
   
2. Given a filename containing an ISO 8601 datetime string, return a Python Dictionary of useful metadata.

3. Given one or more directories of such files, build an array of such Dictionaries.  With the *addition* of Sort Codes, for knowing a file's relative position compared to others, based on datetime.

## Installation
I intend to publish this on PyPi.  In the meantime, you can include a requirement in your *Python Setuptools* setup.py, as follows:
```
os.system('pip install --user git+https://gitlab.com/brian_pond/file8601@master')
```

## Usage

### Add a suffix to a filename

Here is the Python code you would write, to add an ISO 8601 datetime suffix to a file name:

```python
from file8601 import StampFilename
my_file_name = '/home/brian/documentation/myfile_summary.tar.gz'
new_file_name = StampFilename(my_file_name).add_suffix()
```

Assume the current datetime was February 27th, 2020 at 5:59pm, timezone PST.  The above function would return this:
```
myfile_summary_2020-02-27T175900-0800.tar.gz
```

This new, stamped filename can be interpreted by other programs.  My first use-case was my related File Backup tools: [Backbot](https://gitlab.com/brian_pond/backbot) and [Backbot Origin](https://gitlab.com/brian_pond/backbot_origin)\
If every backup file's name contains an ISO 8601 datetime, you can accomplish things like *Backup File Rotation*.

### Decode a suffix
```python
from file8601 import build_file_metadata
my_file_name = 'myfile_summary_2020-03-04T170054-0800.tar.gz'
metadata = build_file_metadata(my_file_name)
print(metadata)
```
Results would be the following Python Dictionary:
```
{
    'path': PosixPath('myfile_summary_2020-03-04T170054-0800.tar.gz'),
    'parentdir': '/home/user/projects/python/file8601.repo',
    'full_name': 'myfile_summary_2020-03-04T170054-0800.tar.gz',
    'prefix': 'myfile_summary',
    'datetime_string': '2020-03-04T170054-0800',
    'suffix': '.tar.gz',
    'orig_datetime': datetime.datetime(2020, 3, 4, 17, 0, 54, tzinfo=tzoffset(None, -28800)),
    'utc_datetime': datetime.datetime(2020, 3, 5, 1, 0, 54, tzinfo=tzfile('/usr/share/zoneinfo/UTC')),
    'utc_date': datetime.date(2020, 3, 5),
    'utc_time': datetime.time(1, 0, 54)
}
```

## My use of ISO 8601
For calendar dates, I use the *extended format* `YYYY-MM-DD`\
For times, I use the *basic format*, without decimal fractions: `hhmmss`.
For time zone designators, I am using the *basic format*: `±hhmm`

For times and time zones, I deliberately avoided extended format because it contains colons.  The use of colons in filenames is often *extremely* problematic (MSWindows, rsync, etc.)

## Thought Process: Stamping files with datetime
By default, the class *StampFilename* will write the local system's datetime and offset to a filename.  I considered always writing UTC, but decided against it.\
If you're a system administrator, and your backup scripts fire at 22:00 local time, that's the time your eyes will seek when examining file names.

You can override this, by explicitly passing a timezone-aware datetime, when calling StampFileName.

Regardless, when building file metadata...
```python
file8601.build_file_metadata(my_file_name)
```
...you can always examine the UTC elements: `utc_datetime`, `utc_date`, `utc_time`.
