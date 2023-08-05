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

# File: /Users/hain/git/compose4py/compose/__init__.py
# Author: Hai Liang Wang
# Date: 2020-03-21:10:16:05
#
#===============================================================================

"""
   
"""
__all__ = ["__copyright__", "__author__", "__date__", "Compose"]

__copyright__ = "Copyright (c) 2020 . All Rights Reserved"
__author__ = "Hai Liang Wang"
__date__ = "2020-03-21:10:16:05"

import os, sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

if sys.version_info[0] < 3:
    raise RuntimeError("Must be using Python 3")
else:
    unicode = str

"""
This module provides some commonly used processors for Item Loaders.

See documentation in docs/topics/loaders.rst
"""
from types import GeneratorType
from collections import ChainMap
from misc import arg_to_iter, wrap_loader_context


# class MapCompose:
#     '''
#     接受多个参数对map，针对参数数组的map运算
#     '''

#     def __init__(self, *functions, **default_loader_context):
#         self.functions = functions
#         self.default_loader_context = default_loader_context

#     def __call__(self, value, loader_context=None):
#         values = arg_to_iter(value)
#         if loader_context:
#             context = ChainMap(loader_context, self.default_loader_context)
#         else:
#             context = self.default_loader_context
#         wrapped_funcs = [wrap_loader_context(f, context) for f in self.functions]
#         for func in wrapped_funcs:
#             next_values = []
#             for v in values:
#                 try:
#                     next_values += arg_to_iter(func(v))
#                 except Exception as e:
#                     raise ValueError("Error in MapCompose with "
#                                      "%s value=%r error='%s: %s'" %
#                                      (str(func), value, type(e).__name__,
#                                       str(e)))
#             values = next_values
#         return values


class Compose:
    '''
    只对单个参数进行运算
    value设置为dict或Object比较好
    '''

    def __init__(self, *functions, **default_loader_context):
        self.functions = functions
        self.stop_on_none = default_loader_context.get('stop_on_none', False)
        self.default_loader_context = default_loader_context

    def __call__(self, value, loader_context=None):
        if loader_context:
            context = ChainMap(loader_context, self.default_loader_context)
        else:
            context = self.default_loader_context
        
        wrapped_funcs = [wrap_loader_context(f, context) for f in self.functions]
        post_funcs = []
        for func in wrapped_funcs:
            if value is None and self.stop_on_none:
                break
            try:
                ret = func(value)
                if isinstance(ret, GeneratorType):
                    post_funcs.append(ret)
                    value = next(ret)
                else: value = ret
            except Exception as e:
                raise ValueError("Error in Compose with "
                                 "%s value=%r error='%s: %s'" %
                                 (str(func), value, type(e).__name__, str(e)))

        for i in reversed(range(len(post_funcs))):
            if value is None and self.stop_on_none:
                break
            try:
                post_funcs[i].send(value)
            except StopIteration as e:
                value =  e.value
            except Exception as e:
                raise ValueError("Error in Compose with "
                                 "%s value=%r error='%s: %s'" %
                                 (str(post_funcs[i]), value, type(e).__name__, str(e)))        

        return value
