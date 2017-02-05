#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from setuptools import setup, find_packages


# define the version string inside the package
# see https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package
VERSIONFILE="motomagic/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


setup(name='motomagic',
      version=version,
      description='Anomaly detection assistant for safer motorbike riding',
      author='Rajesh Venkatachalam, Denys Lazarenko',
      packages=find_packages(),
      include_package_data=True,
      )
