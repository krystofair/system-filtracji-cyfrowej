#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.

from kivy.app import App
from kivy.uix.bubble import Bubble
import kivy.properties as kp
from kivy.uix.label import Label
from kivy.core.window import Window


class CursorPosBubble(Bubble):
    text = kp.StringProperty('0.0x0.0')
    dx = kp.NumericProperty()
    dy = kp.NumericProperty()
    graph = kp.ObjectProperty()
    label = kp.ObjectProperty()
    size_hint = kp.ObjectProperty((None, None))
    arrow_pos = kp.OptionProperty('l')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._const_size = (100, 30)
        self.label = Label(text=self.text, size=self._const_size)
        self.size = self._const_size
        self.add_widget(self.label)
        Window.bind(mouse_pos=self.on_motion)

    def update_text(self):
        self.text = f'{round(self.dx, ndigits=1)}x{round(self.dy, ndigits=1)}'
        self.label.text = self.text

    def on_motion(self, inst, mouse_pos):
        # if (self.graph is not None and (App.get_running_app().menu_was_clicked(*mouse_pos)
        #                                 or App.get_running_app().menus[0].collide_point(*mouse_pos))):
        mm = App.get_running_app().menus[0]
        if mm.collide_point(*mouse_pos):
            self.remove_widget(self.label)
            self.size = (0, 0)
        elif mm.parent.collide_point(*mouse_pos):
            self.add_widget(self.label) if self.label not in self.content.children else None
            self.size = self._const_size
            self.pos = mouse_pos
            if mouse_pos[0] + self.size[0] >= Window.size[0]:
                self.pos[0] -= self.size[0]
            if mouse_pos[1] + self.size[1] >= Window.size[1]:
                self.pos[1] -= self.size[1]
            if self.graph is not None and self.graph.collide_point(*mouse_pos):
                self.dx, self.dy = self.graph.to_data(*self.graph.to_widget(*mouse_pos))
                self.update_text()
