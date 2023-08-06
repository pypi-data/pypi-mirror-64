#!/usr/bin/env python

from setuptools import setup
# import os 
# import re
# # The full version, including alpha/beta/rc tags.
# release = re.sub('^v', '', os.popen('git describe').read().strip())
# # The short X.Y version.
# version = release

setup(
    setup_requires=['pbr>=1.9', 'setuptools>=17.1'],
    pbr=True,
)