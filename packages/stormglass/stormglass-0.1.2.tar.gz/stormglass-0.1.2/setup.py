#!/usr/bin/env python3

import codecs
import os
import re
from setuptools import setup

with open("README.md", "r") as f:
    readme = f.read()

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


_title = "stormglass"
_description = "Python wrapper for the Storm Glass Global weather API"
_author = "Carl Larsson"
_author_email = "cf@stormglass.io"
_license = "MIT"
_url = "https://github.com/caalle/stormglass-python"

setup(
    name=_title,
    description=_description,
    long_description=readme,
    long_description_content_type="text/markdown",
    version=find_version("stormglass", "__init__.py"),
    author=_author,
    author_email=_author_email,
    url=_url,
    packages=["stormglass"],
    include_package_data=True,
    python_requires=">=3.5.*",
    install_requires=["urllib3", "certifi"],
    license=_license,
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 1 - Planning",
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="stormglass,weather,marine weather",
)
