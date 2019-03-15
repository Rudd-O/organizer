#!/usr/bin/python2

from setuptools import setup
import os

dir = os.path.dirname(__file__)
path_to_main_file = os.path.join(dir, "src/organizer/__init__.py")
path_to_readme = os.path.join(dir, "README.md")
for line in open(path_to_main_file):
	if line.startswith('__version__'):
		version = line.split()[-1].strip("'").strip('"')
		break
else:
	raise ValueError, '"__version__" not found in "src/organizer/__init__.py"'
readme = open(path_to_readme).read(-1)

classifiers = [
'Development Status :: 5 - Production/Stable',
'Environment :: Console',
'Environment :: No Input/Output (Daemon)',
'Intended Audience :: End Users/Desktop',
'Intended Audience :: System Administrators',
'License :: OSI Approved :: GNU General Public License (GPL)',
'Operating System :: POSIX :: Linux',
'Programming Language :: Python :: 2 :: Only',
'Programming Language :: Python :: 2.7',
'Topic :: Communications :: File Sharing',
'Topic :: Utilities',
]

setup(
	name = 'organizer',
	version=version,
	description = 'A tool to assist in organizing media files',
	long_description = readme,
	author='Manuel Amador (Rudd-O)',
	author_email='rudd-o@rudd-o.com',
	license="GPL",
	url = 'http://github.com/Rudd-O/organizer',
	package_dir=dict([
					("organizer", "src/organizer"),
					]),
	classifiers = classifiers,
	packages = ["organizer"],
	data_files = [
		("/usr/share/applications", ["organizer.desktop"]),
	],
	scripts = ["bin/organizer"],
	keywords = "organizer media",
	requires = ["iniparse"],
	zip_safe=False,
)
