#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#
# Copyright 2020 (c) Scrapy developers. All rights reserved.
# https://github.com/scrapy/scrapy/blob/master/LICENSE
# Modifications copyright (C) 2020 Chatopera Inc, <https://www.chatopera.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Author: Hai Liang Wang
# Date: 2020-03-21:10:16:05
#
#===============================================================================

"""
   
"""
__copyright__ = "Copyright (c) 2020 . All Rights Reserved"
__author__ = "Hai Liang Wang"
__date__ = "2020-03-21:10:09:46"

import os, sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

if sys.version_info[0] < 3:
    raise RuntimeError("Must be using Python 3")
else:
    unicode = str

"""Helper functions which don't fit anywhere else"""
import ast
import inspect
import re
import hashlib
import warnings
from contextlib import contextmanager
from importlib import import_module
from pkgutil import iter_modules
from textwrap import dedent
from functools import partial

def _getargspec_py23(func):
    """_getargspec_py23(function) -> named tuple ArgSpec(args, varargs, keywords,
                                                        defaults)

    Was identical to inspect.getargspec() in python2, but uses
    inspect.getfullargspec() for python3 behind the scenes to avoid
    DeprecationWarning.

    >>> def f(a, b=2, *ar, **kw):
    ...     pass

    >>> _getargspec_py23(f)
    ArgSpec(args=['a', 'b'], varargs='ar', keywords='kw', defaults=(2,))
    """
    return inspect.ArgSpec(*inspect.getfullargspec(func)[:4])


def get_func_args(func, stripself=False):
    """Return the argument name list of a callable"""
    if inspect.isfunction(func):
        func_args, _, _, _ = _getargspec_py23(func)
    elif inspect.isclass(func):
        return get_func_args(func.__init__, True)
    elif inspect.ismethod(func):
        return get_func_args(func.__func__, True)
    elif inspect.ismethoddescriptor(func):
        return []
    elif isinstance(func, partial):
        return [x for x in get_func_args(func.func)[len(func.args):]
                if not (func.keywords and x in func.keywords)]
    elif hasattr(func, '__call__'):
        if inspect.isroutine(func):
            return []
        elif getattr(func, '__name__', None) == '__call__':
            return []
        else:
            return get_func_args(func.__call__, True)
    else:
        raise TypeError('%s is not callable' % type(func))
    if stripself:
        func_args.pop(0)
    return func_args

def flatten(x):
    """flatten(sequence) -> list

    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, (8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]
    >>> flatten(["foo", "bar"])
    ['foo', 'bar']
    >>> flatten(["foo", ["baz", 42], "bar"])
    ['foo', 'baz', 42, 'bar']
    """
    return list(iflatten(x))


def iflatten(x):
    """iflatten(sequence) -> iterator

    Similar to ``.flatten()``, but returns iterator instead"""
    for el in x:
        if is_listlike(el):
            for el_ in iflatten(el):
                yield el_
        else:
            yield el


def is_listlike(x):
    """
    >>> is_listlike("foo")
    False
    >>> is_listlike(5)
    False
    >>> is_listlike(b"foo")
    False
    >>> is_listlike([b"foo"])
    True
    >>> is_listlike((b"foo",))
    True
    >>> is_listlike({})
    True
    >>> is_listlike(set())
    True
    >>> is_listlike((x for x in range(3)))
    True
    >>> is_listlike(range(5))
    True
    """
    return hasattr(x, "__iter__") and not isinstance(x, (str, bytes))


def unique(list_, key=lambda x: x):
    """efficient function to uniquify a list preserving item order"""
    seen = set()
    result = []
    for item in list_:
        seenkey = key(item)
        if seenkey in seen:
            continue
        seen.add(seenkey)
        result.append(item)
    return result


def to_unicode(text, encoding=None, errors='strict'):
    """Return the unicode representation of a bytes object ``text``. If
    ``text`` is already an unicode object, return it as-is."""
    if isinstance(text, str):
        return text
    if not isinstance(text, (bytes, str)):
        raise TypeError('to_unicode must receive a bytes or str '
                        'object, got %s' % type(text).__name__)
    if encoding is None:
        encoding = 'utf-8'
    return text.decode(encoding, errors)


def to_bytes(text, encoding=None, errors='strict'):
    """Return the binary representation of ``text``. If ``text``
    is already a bytes object, return it as-is."""
    if isinstance(text, bytes):
        return text
    if not isinstance(text, str):
        raise TypeError('to_bytes must receive a str or bytes '
                        'object, got %s' % type(text).__name__)
    if encoding is None:
        encoding = 'utf-8'
    return text.encode(encoding, errors)

class BaseItem(object):
    """Base class for all scraped items.

    In Scrapy, an object is considered an *item* if it is an instance of either
    :class:`BaseItem` or :class:`dict`. For example, when the output of a
    spider callback is evaluated, only instances of :class:`BaseItem` or
    :class:`dict` are passed to :ref:`item pipelines <topics-item-pipeline>`.

    If you need instances of a custom class to be considered items by Scrapy,
    you must inherit from either :class:`BaseItem` or :class:`dict`.

    Unlike instances of :class:`dict`, instances of :class:`BaseItem` may be
    :ref:`tracked <topics-leaks-trackrefs>` to debug memory leaks.
    """
    pass

_ITERABLE_SINGLE_VALUES = dict, BaseItem, str, bytes


def arg_to_iter(arg):
    """Convert an argument to an iterable. The argument can be a None, single
    value, or an iterable.

    Exception: if arg is a dict, [arg] will be returned
    """
    if arg is None:
        return []
    elif not isinstance(arg, _ITERABLE_SINGLE_VALUES) and hasattr(arg, '__iter__'):
        return arg
    else:
        return [arg]

def wrap_loader_context(function, context):
    """Wrap functions that receive loader_context to contain the context
    "pre-loaded" and expose a interface that receives only one argument
    """
    if 'loader_context' in get_func_args(function):
        return partial(function, loader_context=context)
    else:
        return function