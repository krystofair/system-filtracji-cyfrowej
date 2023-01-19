#  Copyright (c) 2023.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.

from menus import FilterMenu
from kivy.logger import Logger
import store


class BandpassBwFilterMenu(FilterMenu):
    pass


def set_order(number):
    try:
        num = int(number) if isinstance(number, str) else number
        store.get('loaded-filter').set_order(num)
    except Exception as e:
        Logger.exception(e)
