#!/usr/bin/env python
# coding: utf-8

# Copyright (c) tjdevries.
# Distributed under the terms of the Modified BSD License.


from pathlib import Path

import toml

# TODO: I'm not sure if this is the best way to keep these in sync, but this is the only way I can think of to grab the thing from pyproject.toml
#   I don't love reading a file on project start though...
pyproject_toml_path = Path(str(__file__)).parent.parent

try:
    version_info = tuple(toml.load(pyproject_toml_path / "pyproject.toml")["tool"]["poetry"]["version"].split("."))
except:
    version_info = (0, 9, 9)

__version__ = ".".join(map(str, version_info))
