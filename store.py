#  Copyright (c) 2023.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.
"""
This is implementation of key-value store.
Keys should be only strings, but here this is not validated.
"""

from kivy.logger import Logger as log


G = globals()
if 'store' in G:
    store = G['store']
else:
    store = {}


def get_store() -> dict:
    return store


def add(key, value) -> bool:
    if key in store:
        log.warn(f'The {value} was not added, because key {key} already exists.')
        return False
    else:
        store[key] = value
        log.info(f'Added {value} to store under key {key}.')
        return True


def add_or_update(key, value):
    if key in store:
        store.update({key: value})
        log.info(f'Update key {key} in store with value {value}.')
    else:
        store[key] = value
        log.info(f'Added new value {value} to store under key {key}.')


def delete(key) -> bool:
    if key in store:
        del store[key]
        log.info(f'Delete key {key} from store')
        return True
    else:
        log.warn(f'There is no key {key} in store.')
        return False


def update(key, value) -> bool:
    if key in store:
        store.update({key: value})
        log.info(f'Update key {key} in store with value {value}.')
        return True
    else:
        log.warn(f'The key {key} was not update, because there is no such a key in store.')
        return False


def get(key):
    if key in store:
        log.info(f"Getting value from store[{key}].")
        return store[key]
    else:
        return None
