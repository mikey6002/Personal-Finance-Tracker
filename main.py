import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class MyGrid():
    pass

class MyApp(App):
    def build(self):
        return MyGrid()
    

if __name__ == "__main__":
    MyApp().run()