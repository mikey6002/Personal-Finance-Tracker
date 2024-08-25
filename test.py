import csv
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
from kivy.properties import StringProperty
from kivymd_extensions.akivymd.uix.charts import AKPieChart

Window.size = (380, 740)

def format_category_name(category_name):
    return category_name.replace('_', ' ').title()

def read_csv_data(file_path, user_email):
    headers = []
    values = []
    income = 0
    total_amount = 0

    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['email'] == user_email:
                    headers = list(row.keys())
                    values = list(row.values())
                    income = int(values[2]) if values[2] else 0
                    break

        formatted_rows_dict = []
        formatted_rows_tuple = []

        for i in range(3, 10):
            category = headers[i]
            amount = values[i]
            if amount:
                total_amount += int(amount)

        if total_amount > 0:
            for i in range(3, 10):
                category = headers[i]
                amount = values[i]
                if amount:
                    formatted_category = format_category_name(category)
                    percentage_of_income = (int(amount) / total_amount) * 100
                    formatted_rows_dict.append({formatted_category: round(percentage_of_income, 2)})
                    formatted_rows_tuple.append((formatted_category, amount))

            if formatted_rows_dict:
                total_percentage = sum(d[list(d.keys())[0]] for d in formatted_rows_dict)
                if total_percentage < 100:
                    last_entry = formatted_rows_dict[-1]
                    last_key = list(last_entry.keys())[0]
                    last_entry[last_key] += (100 - total_percentage)

    except Exception as e:
        print(f"Error reading CSV file: {e}")

    return income, total_amount, formatted_rows_dict, formatted_rows_tuple

class SpendingTrackerApp(MDApp):
    income_display = StringProperty("$0")

    def build(self):
        return Builder.load_file('spendingtracker.kv')

    def on_start(self):
        self.income, total_amount, formatted_rows_dict, formatted_rows_tuple = read_csv_data('user_data(1).csv', 'Barrylin@gmail.com')
        self.items = [{key: value for d in formatted_rows_dict for key, value in d.items()}]

        self.piechart = AKPieChart(
            items=self.items,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=[None, None],
            size=(dp(180), dp(180)),
        )
        self.root.ids.chart_box.add_widget(self.piechart)

        category_list = self.root.ids.category_list
        for category, amount in formatted_rows_tuple:
            formatted_amount = f"${int(amount):,}".rjust(20)
            item = OneLineListItem(text=f"{category:<25}{formatted_amount}")
            category_list.add_widget(item)

        # Format income and total amount and update the property
        total_expenses = total_amount + self.income
        self.income_display = f"Total Expenses\n${total_amount:,}\nCurrent Income\n${self.income:,}"

    def remove_chart(self):
        self.root.ids.chart_box.remove_widget(self.piechart)

if __name__ == '__main__':
    SpendingTrackerApp().run()
