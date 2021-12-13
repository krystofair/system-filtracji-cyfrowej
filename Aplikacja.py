# imports
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.app import App
from kivy.utils import interpolate

# poniższy import nie istnieje w virtualenv
# from scipy import interpolate 

class CustomButton(Button):
    def on_press(self):
        pass


class Aplikacja(App):
    pass

if __name__ == '__main__':
    Aplikacja().run()
