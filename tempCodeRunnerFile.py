from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import MDList, OneLineListItem
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.lang import Builder

Window.size = (360, 740)

class SpendingTracker(MDBoxLayout):
    pass

class SpendingTrackerApp(MDApp):
    def build(self):
        Builder.load_file('spendingtracker.kv')

    def on_start(self):
        categories = [
            ("Food & Drink", "$200.00"),
            ("Shopping", "$5,200,000"),
            ("Entertainment", "$3,200,000")
        ]

        category_list = self.root.ids.category_list
        for category, amount in categories:
            item = OneLineListItem(text=f"{category:<25} {amount}")
            category_list.add_widget(item)

if __name__ == '__main__':
    SpendingTrackerApp().run()
