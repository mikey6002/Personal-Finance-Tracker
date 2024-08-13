from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.core.window import Window

Window.size = (310, 580)

KV = '''
Screen:

    MDCard:
        size_hint: None, None
        size: 280, 500
        md_bg_color: [0.0, 0.5, 1.0, 1.0]
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 10
        padding: 15
        spacing: 15
        orientation: 'vertical'

        MDLabel:
            id: opening_label
            text: "Transactions"
            font_size: 24
            halign: 'left'
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 10

        BoxLayout:
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
            padding: 5, 0

            MDRaisedButton:
                id: dates
                size_hint: None, None
                size: 110, 40
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                text: 'Pick Dates'
                color: (1, 1, 1, 1)
                on_release: app.dates_dropper()
                text_size: self.size
                padding_x: 10
                halign: 'left'
            
            MDRaisedButton:
                id: categories
                size_hint: None, None
                size: 110, 40
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                text: 'All Categories'
                color: (1, 1, 1, 1)
                on_release: app.categories_dropper()
                text_size: self.size
                padding_x: 10
                halign: 'right'

        MDBoxLayout:
            id: data_table_box
            size_hint_y: None
            height: dp(250)
'''

class MainApp(MDApp):
    def build(self):
        self.title = "Transactions"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "LightBlue"
        
        root = Builder.load_string(KV)
        
        data_table = MDDataTable(
            size_hint=(1, None),
            height=dp(250),
            use_pagination=False,
            column_data=[
                ("Name", dp(60)),
                ("Date", dp(60)),
                ("Amount", dp(60)),
            ],
            row_data=[
                ("Amazon", "08/10", "$50.00"),
                ("Gas Station", "08/09", "$30.00"),
                ("Grocery Store", "08/08", "$80.00"),
                ("Dining", "08/07", "$45.00"),
                ("Online Shop", "08/06", "$20.00"),
            ]
        )

        root.ids.data_table_box.add_widget(data_table)
        return root
    
    def dates_dropper(self):
        menu_items = [
            {"text": "Last 7 days", "on_release": lambda x="Last 7 days": self.menu_callback('dates', x)},
            {"text": "Last 14 days", "on_release": lambda x="Last 14 days": self.menu_callback('dates', x)},
        ]
        self.menu = MDDropdownMenu(
            caller=self.root.ids.dates,
            items=menu_items,
            width_mult=3
        )
        self.menu.open()
    
    def categories_dropper(self):
        menu_items = [
            {"text": "Online Shopping", "on_release": lambda x="Online Shopping": self.menu_callback('categories', x)},
            {"text": "Dining", "on_release": lambda x="Dining": self.menu_callback('categories', x)},
            {"text": "Utilities", "on_release": lambda x="Utilities": self.menu_callback('categories', x)},
            {"text": "Gas & EV Charging", "on_release": lambda x="Gas & EV Charging": self.menu_callback('categories', x)},
        ]
        self.menu = MDDropdownMenu(
            caller=self.root.ids.categories,
            items=menu_items,
            width_mult=3
        )
        self.menu.open()

    def menu_callback(self, widget_id, text_item):
        self.root.ids[widget_id].text = text_item  # Update the button's text
        self.menu.dismiss()

MainApp().run()
