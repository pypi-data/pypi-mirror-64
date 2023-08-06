#!/usr/bin/env python
import codecs
import os.path
import re
import sys

import shutil
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


requires = [
            'configparser>=3.5.0',
            'six',
            'fabric==1.14.0',
            'setuptools',
            'cryptography>=2.4.2'
]
if sys.platform == 'win32':
    requires.append('pywin32')

if sys.version_info[:2] == (2, 6):
    # For python2.6 we have to require argparse since it
    # was not in stdlib until 2.7.
    requires.append('argparse>=1.1')


setup_options = dict(
    name='fablinker',
    version=find_version("fablinker", "constant.py"),
    description='A tool for operating servers.',
    long_description=open('README.rst').read(),
    author='GaryLi',
    author_email='gangly123@163.com',
    url='https://github.com/gangly/fablinker',
    scripts=['bin/fablinker',
             ],
    packages=find_packages(exclude=['tests*']),
    package_data={'fablinker': ['data/*.json', 'data/*.ini', 'examples/*/*.rst',
                             'examples/*/*/*.rst']},
    install_requires=requires,
    extras_require={
        ':python_version=="2.6"': [
            'argparse>=1.1',
        ]
    },
    license="Apache License 2.0",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)


def get_full_path(path):
    fullpath = os.path.expandvars(path)
    fullpath = os.path.expanduser(fullpath)
    fullpath = os.path.abspath(fullpath)
    return fullpath

FABLINKER_DIR = get_full_path(os.path.join('~', '.fablinker'))
CONFIG_FILE = os.path.join(FABLINKER_DIR, 'fabconf.ini')
# DEFAULT_CONFIG_FILE = os.path.join(FABLINKER_DIR, 'default.ini')

ROOT_DIR = os.path.dirname(__file__)
HCMD_INI = os.path.join(ROOT_DIR, 'fablinker', 'data', 'fabconf.ini')


if not os.path.exists(FABLINKER_DIR):
    os.makedirs(FABLINKER_DIR)
# shutil.copyfile(HCMD_INI, DEFAULT_CONFIG_FILE)
if not os.path.exists(CONFIG_FILE):
    shutil.copyfile(HCMD_INI, CONFIG_FILE)

if 'py2exe' in sys.argv:
    # This will actually give us a py2exe command.
    import py2exe
    # And we have some py2exe specific options.
    setup_options['options'] = {
        'py2exe': {
            'optimize': 0,
            'skip_archive': True,
            'dll_excludes': ['crypt32.dll'],
            'packages': ['urllib', 'httplib', 'HTMLParser',
                         'fablinker', 'ConfigParser', 'xml.etree', 'pipes'],
        }
    }
    setup_options['console'] = ['bin/fablinker']


BIN_HCMD = '/usr/bin/fablinker'
LOCAL_HCMD = '/usr/local/bin/fablinker'
if sys.platform != 'win32' and os.path.exists(BIN_HCMD):
    os.remove(BIN_HCMD)
if sys.platform != 'win32' and os.path.exists(LOCAL_HCMD):
    os.remove(LOCAL_HCMD)

setup(**setup_options)

if sys.platform != 'win32' and os.path.exists(BIN_HCMD) and not os.path.exists(LOCAL_HCMD):
    os.symlink(BIN_HCMD, LOCAL_HCMD)