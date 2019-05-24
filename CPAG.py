import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window


class MainGrid(GridLayout):
    pass


class CPAG(App):
    def build(self):
        Window.Clearcolour = (1, 1, 1, 1)
        return MainGrid()


app = CPAG()
app.run()
