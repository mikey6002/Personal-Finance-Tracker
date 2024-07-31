from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu


from kivy.core.window import Window
Window.fullscreen = False
Window.size = (360, 640)

class MD3Card(MDCard):
    
    text = StringProperty()

class MobileView(MDScreen):
    pass

class Example(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"
        return Builder.load_file('Card.kv')

    def on_start(self):
        # Add a card to the mobile view
        self.root.ids.box.add_widget(
            MD3Card(
                line_color=(0.2, 0.2, 0.2, 0.8),
                text="Credit Card",
                md_bg_color="#f4dedc",
                shadow_softness=0,
                shadow_offset=(0, 0),
            )
        )

        #  dropdown menu items with specific labels
        menu_items = [
            {
                "text": "Edit",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.menu_callback("Edit"),
            },
            {
                "text": "Add new card",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.menu_callback("Add new card"),
            },
        ]
        
        
        # Initialize MDDropdownMenu
        self.menu = MDDropdownMenu(
            caller=None,  # Initially set to None
            items=menu_items,
            width_mult=4,
        )

    def menu_callback(self, text_item):
        print(text_item)

    def open_menu(self, button):
        self.menu.caller = button  # Set the caller to the button
        self.menu.open()

Example().run()
