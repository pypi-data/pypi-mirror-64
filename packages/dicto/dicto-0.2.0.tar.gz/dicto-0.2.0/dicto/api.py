"""
DCDD
"""

import collections
import copy
import functools
import json
import os
import typing
from pathlib import Path

import xmltodict
import yaml


class Dicto(object):
    """
    ABC
    """

    def __init__(self, dict_: dict = None, **kwargs):
        """
        Creates a Dicto instance from a `dict` recursively, that is, inner fields of type, `dict`, `list`, `tuple`, and `set` and traversed and all `dict` objects found at any point are converted to a Dicto.

        Parameters:
            dict_: a `dict` object (or any object accepted by `dict`s constructor) to be converted to a Dicto.
            kwargs: just like in `dict`, all keyword arguments are added as fields.
        """

        if dict_ is None:
            dict_ = {}
        elif not isinstance(dict_, dict):
            dict_ = dict(dict_)

        dict_.update(kwargs)

        to_dicto(dict_, dicto=self)

    def __setitem__(self, key, item):
        setattr(self, key, item)

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return repr(vars(self))

    def __len__(self):
        return len(vars(self))

    def __delitem__(self, key):
        delattr(self, key)

    def __contains__(self, item):
        return hasattr(self, item)

    def __iter__(self):
        return iter(vars(self))


def to_dicto(obj, dicto=None):

    if isinstance(obj, Dicto):
        return obj

    elif isinstance(obj, dict):

        if dicto is None:
            dicto = Dicto()

        for key, value in obj.items():

            value = to_dicto(value)

            setattr(dicto, key, value)

        return dicto

    elif isinstance(obj, list):
        return [to_dicto(x) for x in obj]

    elif isinstance(obj, tuple):
        return tuple([to_dicto(x) for x in obj])

    elif isinstance(obj, set):
        return {to_dicto(x) for x in obj}
    else:
        return obj


def to_dict(obj: typing.Any, dict_=None):
    """
    Converts a Dicto object to a `dict` recursively, that is, inner fields of type Dicto, `dict`, `list`, `tuple`, and `set` and traversed and all Dicto objects found at any point are converted to `dict`.

    Parameters:
        obj: a Dicto, `dict`, `list`, `tuple`, or `set` object to be parsed to a `dict`, objects of other types are returned as is.
    """

    if isinstance(obj, dict):
        return {key: to_dict(value) for key, value in obj.items()}

    elif isinstance(obj, Dicto):

        if dict_ is None:
            dict_ = dict()

        for key, value in vars(obj).items():

            dict_[key] = to_dict(value)

        return dict_

    elif isinstance(obj, list):
        return [to_dict(x) for x in obj]

    elif isinstance(obj, tuple):
        return tuple([to_dict(x) for x in obj])

    elif isinstance(obj, set):
        return {to_dict(x) for x in obj}

    else:
        return obj


def merge(dicto, other):

    if not isinstance(dicto, Dicto):
        dicto = Dicto(dicto)

    if not isinstance(other, Dicto):
        other = Dicto(other)

    for k, v in other.__dict__.items():
        if k in dicto and isinstance(dicto[k], Dicto) and isinstance(other[k], Dicto):
            dicto[k] = merge(dicto[k], other[k])
        else:
            dicto[k] = other[k]

    return dicto


def load(filepath: Path) -> Dicto:
    """
    Loads a Dicto from a config file. Currently the following extension are valid:

    * `.json`
    * `.yaml` or `.yml`
    * `.xml

    Parameters:
        filepath: a `pathlib.Path` or `str` containing the path to the config file.
    
    Returns:
        A Dicto instance.
    """
    if not isinstance(filepath, Path):
        filepath = Path(filepath)

    if filepath.suffix in (".yaml", ".yml"):

        with open(filepath, "r") as stream:
            dict_ = yaml.safe_load(stream)

    elif filepath.suffix == ".json":

        with open(filepath, "r") as stream:
            dict_ = json.load(stream)

    elif filepath.suffix == ".xml":

        with open(filepath, "r") as stream:
            dict_ = xmltodict.parse(stream.read())

    else:
        raise Exception("File type not supported.")

    return to_dicto(dict_)


def dump(dicto: Dicto, filepath: Path):
    """
    Serializes a Dicto instance to a config file. Currently the following extension are valid:

    * `.json`
    * `.yaml` or `.yml`

    Parameters:
        dicto: a Dicto instance to be serialized.
        filepath: a `pathlib.Path` or `str` containing the path to the config file.
    """

    if not isinstance(filepath, Path):
        filepath = Path(filepath)

    obj = to_dict(dicto)

    if filepath.suffix in (".yaml", ".yml"):
        with open(filepath, "w") as stream:
            yaml.safe_dump(obj, stream, default_flow_style=False)

    elif filepath.suffix == ".json":
        with open(filepath, "w") as stream:
            json.dump(obj, stream)
    else:
        raise Exception("File type not supported.")
