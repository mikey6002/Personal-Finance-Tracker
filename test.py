from kivy.app import App
from kivy.uix.label import Label 
class BasicApp(App):
    def build(self):
        return Label(text="Hello World! This is testing the branch")
if __name__ == "__main__":
    BasicApp().run()
    
    