#!/usr/bin/env python

import fnmatch
import os
import tarfile
import argparse

excluded_patterns = [
	"*.pyc", "*.pyo", "*.so", "*.pc", "*.a", "*.la",
	"lib/python2.7/BaseHTTPServer.py",
	"lib/python2.7/Bastion.py",
	"lib/python2.7/Cookie.py",
	"lib/python2.7/CGIHTTPServer.py",
	"lib/python2.7/DocXMLRPCServer.py",
	"lib/python2.7/HTMLParser.py",
	"lib/python2.7/MimeWriter.py",
	"lib/python2.7/SimpleHTTPServer.py",
	"lib/python2.7/SimpleXMLRPCServer.py",
	"lib/python2.7/SocketServer.py",
	"lib/python2.7/_LWPCookieJar.py",
	"lib/python2.7/_MozillaCookieJar.py",
	"lib/python2.7/__phello__.foo.py",
	"lib/python2.7/_threading_local.py",
	"lib/python2.7/aifc.py",
	"lib/python2.7/antigravity.py",
	"lib/python2.7/anydbm.py",
	"lib/python2.7/decimal.py",
	"lib/python2.7/doctest.py",
	"lib/python2.7/mailbox.py",
	"lib/python2.7/difflib.py",
	"lib/python2.7/cookielib.py",
	"lib/python2.7/optparse.py",
	"lib/python2.7/nturl2path.py",
	"lib/python2.7/os2emxpath.py",
	"lib/python2.7/_osx_support.py",
	"lib/python2.7/pydoc.py",
	"lib/python2.7/robotparser.py",
	"lib/python2.7/sndhdr.py",
	"lib/python2.7/stringold.py",
	"lib/python2.7/stringprep.py",
	"lib/python2.7/subprocess.py",
	"lib/python2.7/sunau.py",
	"lib/python2.7/sunaudio.py",
	"lib/python2.7/tabnanny.py",
	"lib/python2.7/tarfile.py",
	"lib/python2.7/telnetlib.py",
	"lib/python2.7/threading.py",
	"lib/python2.7/toaiff.py",
	"lib/python2.7/wave.py",
	"lib/python2.7/webbrowser.py",
	"lib/python2.7/whichdb.py",
	"lib/python2.7/xdrlib.py",
	"lib/python2.7/xmllib.py",
	"lib/python2.7/xmlrpclib.py",
	"lib/python2.7/uu.py",
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
	"lib/python2.7/ensurepip",
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
	"lib/python2.7/json/tests",
	"share",
	"include",
]

def check_directories(filename):
	return not any(filename.startswith(directory + "/") for directory in excluded_directories)


def main(prefix_dir, output_path):
	filtered_filenames = []
	for (directory, _, filenames) in os.walk(prefix_dir):
		relative_filenames = filter(check_filename, [os.path.relpath(os.path.join(directory, filename), prefix_dir) for filename in filenames])
		absolute_filenames = [os.path.join(prefix_dir, filename) for filename in relative_filenames]
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

