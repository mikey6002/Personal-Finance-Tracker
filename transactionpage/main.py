from kivy.lang import Builder
from kivymd.app import MDApp 
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

class MainApp(MDApp):


    def build(self):
        self.title = "Transactions"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "LightBlue"
        return Builder.load_file('transaction.kv')
    

    def dates_dropper(self):
        menu_items = [
            {
                "text": "Last 7 days",
                "on_release": lambda x="Last 7 days": self.menu_callback('dates', x),
            },
            {
                "text": "Last 14 days",
                "on_release": lambda x="Last 14 days": self.menu_callback('dates', x),
            }
        ]
        self.menu = MDDropdownMenu(
            caller=self.root.ids.dates,
            items=menu_items,
            width_mult=4
        )
        self.menu.open()
    
    def categories_dropper(self):
        menu_items = [
            {
                "text": "Online Shopping",
                "on_release": lambda x="Online Shopping": self.menu_callback('categories', x),
            },
            {
                "text": "Dining",
                "on_release": lambda x="Dining": self.menu_callback('categories', x),
            },
            {
                "text": "Utilities",
                "on_release": lambda x="Utilities": self.menu_callback('categories', x),
            },
            {
                "text": "Gas & EV Charging",
                "on_release": lambda x="Gas & EV Charging": self.menu_callback('categories', x),
            },
        ]
        self.menu = MDDropdownMenu(
            caller=self.root.ids.categories,
            items=menu_items,
            width_mult=4
        )
        self.menu.open()

    def menu_callback(self, widget_id, text_item):
        print(text_item)
        self.root.ids[widget_id].text = text_item  # Update the button's text
        self.menu.dismiss()


    
MainApp().run()