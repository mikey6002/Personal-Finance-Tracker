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
from kivymd_extensions.akivymd.uix.charts import AKPieChart

Window.size = (360, 740)

class SpendingTracker(MDBoxLayout):
    pass

class SpendingTrackerApp(MDApp):
    def build(self):
        Builder.load_file('spendingtracker.kv')

    def on_start(self):
        self.items = [{"Shopping": 62, "Entertainment": 37, "Food & Drink": 1}]
        self.piechart = AKPieChart(
            items=self.items,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=[None, None],
            size=(dp(175), dp(175)),
        )
        self.root.ids.chart_box.add_widget(self.piechart)

        categories = [
            ("Monthly Bills", "$200.00"),
            ("Loans", "$5,200,000"),
            ("Entertainment", "$3,200,000")
            ("Rent", "$200.00"),
            ("Groceries", "$5,200,000"),
            ("Misc", "$3,200,000")
        ]

        category_list = self.root.ids.category_list
        for category, amount in categories:
            item = OneLineListItem(text=f"{category:<25} {amount:>21}")
            category_list.add_widget(item)

    def remove_chart(self):
        self.root.ids.chart_box.remove_widget(self.piechart)

if __name__ == '__main__':
    SpendingTrackerApp().run()