#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .constants import (
    FINISHED,
    PENDING,
    RUNNING
)
from .exceptions import ScrapydError
from .wrapper import ScrapydAPI


__version__ = '1.0.1'
__author__ = "william"
__author_email__ = "william.ren@live.cn"
__url__ = "https://github.com/williamren"
__platforms__ = "Any"
__license__ = "Apache License 2.0"
__copyright__ = "Copyright 2001-2017 william william.ren@live.cn"


__all__ = [
    "__version__",
    "__author__",
    "__author_email__",
    "__url__",
    "__platforms__",
    "__license__",
    "__copyright__",

    'ScrapydError',
    'ScrapydAPI',
    'FINISHED',
    'PENDING',
    'RUNNING',
]
