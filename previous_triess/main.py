import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

class MyGrid(Widget):
    name = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    re_type_password = ObjectProperty(None)

    def btn(self):
        print("Name: ", self.name.text, "Email: ", self.email.text, "Password: ", self.password.text, "Re-type Password: ", self.re_type_password.text)
        self.name.text = ""
        self.email.text = ""
        self.password.text = ""
        self.re_type_password.text = ""


class MyApp(App):
    def build(self):
        return MyGrid()
    
if __name__ == "__main__":
    MyApp().run()