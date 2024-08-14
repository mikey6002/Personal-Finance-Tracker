from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime, date

# Scale down the iPhone 14 Pro Max resolution for development
Window.size = (430, 932)  # Scaled-down resolution for development

KV = '''
Screen:

    MDCard:
        size_hint: None, None
        size: 400, 700
        md_bg_color: [0.0, 0.5, 1.0, 1.0]
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 10
        padding: 15
        spacing: 15
        orientation: 'vertical'

        MDLabel:
            id: opening_label
            text: "Transactions"
            font_size: 26
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
                size: 160, 50
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                text: 'Pick Dates'
                color: (1, 1, 1, 1)
                on_release: app.show_date_picker()
                text_size: self.size
                padding_x: 10
                halign: 'left'
            
            MDRaisedButton:
                id: categories
                size_hint: None, None
                size: 160, 50
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
            height: dp(350)
'''

class MainApp(MDApp):
    def build(self):
        self.title = "Transactions"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        
        self.root = Builder.load_string(KV)
        
        self.data_table = MDDataTable(
            size_hint=(1, None),
            height=dp(350),
            use_pagination=False,
            column_data=[
                ("Date", dp(13)),
                ("Name", dp(35)),
                ("Amount", dp(19)),
            ],
            row_data=[
                ("08/10", "Amazon", "$50.00"),
                ("08/09", "Gas Station", "$30.00"),
                ("08/08", "Grocery Store", "$80.00"),
                ("08/07", "Dining", "$45.00"),
                ("08/06", "Other", "$20.00"),
                ("08/06", "Other", "$20.00")
            ]
        )

        self.root.ids.data_table_box.add_widget(self.data_table)
        return self.root

    def show_date_picker(self):
        # Open the date picker dialog
        date_dialog = MDDatePicker(
            mode="range", 
            min_date=date(2023, 1, 1),  # Use datetime.date here
            max_date=date(2023, 12, 31)  # Use datetime.date here
        )

        # Set a custom size for the date picker dialog
        date_dialog.width = dp(350)  # Adjusted width 
        date_dialog.height = dp(400)  # Adjusted height 

        date_dialog.bind(on_save=self.on_save_date_picker)
        date_dialog.open()

    def on_save_date_picker(self, instance, value, date_range):
        # When the date is selected, update the button text and filter the data
        if date_range:
            start_date = date_range[0]
            end_date = date_range[-1]
            self.root.ids.dates.text = f"{start_date.strftime('%m/%d')} - {end_date.strftime('%m/%d')}"
            self.filter_data_by_date(start_date, end_date)

    def filter_data_by_date(self, start_date, end_date):
    # Sample data for demonstration, assuming these are in '%m/%d' format
        all_data = [
            ("08/10", "Amazon", "$50.00"),
            ("08/09", "Gas Station", "$30.00"),
            ("08/08", "Grocery Store", "$80.00"),
            ("08/07", "Dining", "$45.00"),
            ("08/06", "Other", "$20.00"),
            ("08/06", "Other", "$20.00")
        ]

        # Add a year to the date string and convert to datetime.date objects
        year = start_date.year  # Assume the same year for all dates
        filtered_data = []

        for date_str, name, amount in all_data:
            # Convert '08/10' to '08/10/2023'
            full_date_str = f"{date_str}/{year}"
            try:
                full_date = datetime.strptime(full_date_str, '%m/%d/%Y').date()
            except ValueError as e:
                print(f"Error parsing date: {e}")
                continue

            # Check if the date falls within the selected range
            if start_date <= full_date <= end_date:
                filtered_data.append((date_str, name, amount))

        # Clear the table and add the filtered data
        self.data_table.row_data = filtered_data


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
