#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.
import inspect
import sys, os
import importlib
import logging

from . import filter

# sys.path.append('filters')

log = logging.getLogger()
log.setLevel(logging.INFO)

FILTER_LIST = []

try:
    for e in os.scandir('filters'):
        if e.name == 'filter.py' or e.name == '__init__.py':
            continue
        if e.name.endswith('.py'):
            name_module = 'filters.' + e.name.rstrip('.py')
            module = importlib.import_module(name_module)
            for d in dir(module):
                obj_from_module = getattr(module, d)
                try:
                    # checking IFilter exists in MRO of class by duck typing.
                    not_the_IFilter_itself = obj_from_module is not filter.IFilter 
                    isclass = inspect.isclass(obj_from_module)
                    if isclass and not_the_IFilter_itself:
                        if issubclass(obj_from_module, filter.IFilter):
                            FILTER_LIST.append(obj_from_module)
                except AttributeError:
                    log.info("There was not an mro method for object. Not a class.")
                    continue  # this was not class ;)
except Exception as e:
    print(e)
    raise
