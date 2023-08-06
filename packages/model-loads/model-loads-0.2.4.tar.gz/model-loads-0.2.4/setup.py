#!/usr/bin/env python
import codecs
import os
import re
import sys
from distutils.core import setup

from setuptools import find_packages

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def setup_package():
    src_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(src_path)
    sys.path.insert(0, src_path)

    setup(name='model-loads',
          version=find_version("model_loads", "__init__.py"),
          long_description=long_description,  # Optional
          long_description_content_type='text/markdown',  # Optional (see note above)

          url='https://github.com/cwh94/model_loads',  # Optional
          description='Loads GPU or CPU pytorch models',
          author='wangchao',
          author_email='chaowanghs@gmail.com',
          packages=find_packages(),
          )


if __name__ == "__main__":
    setup_package()
