from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationrail import (
    MDNavigationRailItem,
    MDNavigationRail,
    MDNavigationRailMenuButton,
    MDNavigationRailFabButton,
    MDNavigationRailItemIcon,
    MDNavigationRailItemLabel,
)

class Navbar(MDBoxLayout):
    pass


class MainApp(MDApp):
    def build(self):
        Builder.load_file("my.kv")
        return Navbar()
    
MainApp().run()
