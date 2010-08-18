#!/usr/bin/env python3
#
# python-porcelain: framework for Git porcelain

import os
from distutils.core import setup
from subprocess import Popen, PIPE

git_describe = [ "git", "describe", "--always", "--tags" ]
b = Popen(git_describe, stdout=PIPE).communicate()[0]
s = b.decode()
v = s.strip().replace('v','').replace('-','.')

m = '''# this is a generated file, do not edit
__version__ = "%s"
''' % v

with open('porcelain/__version__.py', 'w+') as f:
    f.write(m)

setup(	name = "python-porcelain",
	version = v,
	description = "framework for Git porcelain",
	author = "Tom Grennan",
	author_email = "tom.grennan@ericsson.com",
	download_url = "git://rbos-git.redback.com/python-porcelain.git",
	packages = ["porcelain"],
	data_files = [('share/doc/python-porcelain',
	    ['COPYING', 'COPYRIGHT', 'INSTALL', 'README'])],
	license = "Copyright (C) 2010 Ericsson, AB" \
		", Licensed under the GPL version 2"
)
