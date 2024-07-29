from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import MDList, OneLineListItem
from kivy.core.window import Window
from kivy.metrics import dp

Window.size = (360, 740)

class SpendingTrackerApp(MDApp):
    def build(self):
        main_layout = BoxLayout(orientation='vertical')

        # Spending Tracker Label
        tracker_label = MDLabel(
            text="Spending Tracker",
            halign='center',
            font_style='H4',
            size_hint_y=None,
            height=dp(60)
        )
        main_layout.add_widget(tracker_label)

        # Expenses Label
        expenses_label = MDLabel(
            text="Expenses",
            halign='center',
            font_style='H5',
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(expenses_label)

        # Button Layout
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            padding=dp(10),
            spacing=dp(10)
        )

        buttons = ["1M", "6M", "1Y", "ALL TIME"]
        for button_text in buttons:
            button = MDRaisedButton(
                text=button_text,
                md_bg_color=self.theme_cls.primary_color if button_text == "ALL TIME" else None
            )
            button_layout.add_widget(button)
        main_layout.add_widget(button_layout)

        # Total Expenses Card
        expenses_card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(300), dp(300)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=dp(10)
        )

        expenses_card_label = MDLabel(
            text="ALL TIME\nTOTAL EXPENSES\n$20,210,230.32",
            halign='center',
            font_style='H5',
            size_hint_y=None,
            height=dp(100),
            padding=(dp(10), dp(10))
        )
        expenses_card.add_widget(expenses_card_label)
        main_layout.add_widget(expenses_card)

        # Top Spending Categories Label
        spending_categories_label = MDLabel(
            text="Top Spending Categories",
            halign='center',
            font_style='H5',
            size_hint_y=None,
            height=dp(40),
            padding=(dp(10), dp(10))
        )
        main_layout.add_widget(spending_categories_label)

        # Scroll View for Categories
        scroll_view = ScrollView(do_scroll_x=False)
        category_list = MDList()

        categories = [
            ("Food & Drink", "$200.00"),
            ("Shopping", "$5,200,000"),
            ("Entertainment", "$3,200,000")
        ]

        for category, amount in categories:
            item = OneLineListItem(text=f"{category:<25} {amount}")
            category_list.add_widget(item)

        scroll_view.add_widget(category_list)
        main_layout.add_widget(scroll_view)

        return main_layout

SpendingTrackerApp().run()
