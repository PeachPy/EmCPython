#!/usr/bin/env python

import fnmatch
import os
import tarfile
import argparse

excluded_patterns = [
	"*.pyc", "*.pyo", "*.so", "*.pc", "*.a", "*.la",
	"lib/python2.7/BaseHTTPServer.py",
	"lib/python2.7/CGIHTTPServer.py",
	"lib/python2.7/DocXMLRPCServer.py",
	"lib/python2.7/HTMLParser.py",
	"lib/python2.7/MimeWriter.py",
	"lib/python2.7/SimpleHTTPServer.py",
	"lib/python2.7/SimpleXMLRPCServer.py",
	"lib/python2.7/antigravity.py",
	"lib/python2.7/os2emxpath.py",
	"lib/python2.7/_osx_support.py"
]
included_patterns = ["*.py"]

def check_filename(filename):
	return any(fnmatch.filter([filename], pattern) for pattern in included_patterns) and \
		not any(fnmatch.filter([filename], pattern) for pattern in excluded_patterns)

excluded_directories = [
	"bin",
	"lib/python2.7/ctypes",
	"lib/python2.7/email",
	"lib/python2.7/test",
	"lib/python2.7/idlelib",
	"lib/python2.7/lib-tk",
	"lib/python2.7/distutils",
	"lib/python2.7/lib2to3",
	"lib/python2.7/wsgiref",
	"lib/python2.7/pydoc_data",
	"lib/python2.7/unittest",
	"lib/python2.7/bsddb",
	"lib/python2.7/hotshot",
	"lib/python2.7/multiprocessing",
	"lib/python2.7/config",
	"lib/python2.7/sqlite3",
	"lib/python2.7/curses",
	"share",
	"include",
]

def check_directories(filename):
	return not any(filename.startswith(directory + "/") for directory in excluded_directories)


def main(prefix_dir, output_path):
	filtered_filenames = []
	for (directory, _, filenames) in os.walk(prefix_dir):
		filenames = filter(check_filename, filenames)
		absolute_filenames = [os.path.join(directory, filename) for filename in filenames]
		relative_filenames = [os.path.relpath(filename, prefix_dir) for filename in absolute_filenames]
		filtered_filenames += filter(check_directories, relative_filenames)

	with tarfile.open(name=output_path, mode='w') as tar_file:
		for filename in filtered_filenames:
			source_filename = os.path.join(prefix_dir, filename)
			print(filename)
			destination_filename = filename
			tar_file.add(source_filename, destination_filename)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Python module repacker")
	parser.add_argument("-p", "--prefix", dest="prefix", required=True,
		help="Python installation prefix")
	parser.add_argument("-o", "--output", dest="output", required=True,
		help="Output path")

	options = parser.parse_args()
	main(options.prefix, options.output)

