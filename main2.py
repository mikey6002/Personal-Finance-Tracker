import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget



class My2App(App):

    class Touch(Widget):

        def on_touch_down(self, touch):
            print("Mouse Down", touch)
    
        def on_touch_move(self, touch):
            print("Mouse Move", touch)
    
        def on_touch_up(self, touch):
            print("Mouse Up", touch)

        def build(self):
           return FloatLayout()
    

if __name__ == "__main__":
    My2App().run()