from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd_extensions.akivymd.uix.charts import AKPieChart
from kivymd.uix.datatables import MDDataTable
import csv
import os


Window.fullscreen = False
Window.size = (380, 740)

class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class Example(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('Dash.kv')

    def on_start(self):
        # Load data from the CSV file 
        csv_file_path = 'user_data.csv'  # path of file
        if not os.path.exists(csv_file_path):
            print(f"File {csv_file_path} not found.")
            return

        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            row = next(reader)  # Assuming only one row of data
            
            # Sum up all the values except "Income"
            total = sum(float(value) for key, value in row.items() if key != "Income")
            
            # Calculate percentages for pie chart
            self.items = [{key: (float(value) / total) * 100 for key, value in row.items() if key != "Income"}]

        # Create the pie chart with the CSV data
        self.piechart = AKPieChart(
            items=self.items,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=[None, None],
            size=(dp(150), dp(150)),
        )
        self.root.ids.chart_box.add_widget(self.piechart)

        # Prepare data for the table
        table_data = []
        for key, value in row.items():
            if key != "Income":
                table_data.append((key, f"${float(value):.2f}"))

        # Create and add the datatable
        self.data_table = MDDataTable(
            size_hint=(None, None),
            size=(dp(300), dp(400)),
            use_pagination=True,
            column_data=[
                ("Category", dp(40)),
                ("Amount", dp(30)),
            ],
            row_data=table_data,
        )
        self.root.ids.data_table_box.add_widget(self.data_table)

    def remove_chart(self):
        self.root.ids.chart_box.remove_widget(self.piechart)

if __name__ == '__main__':
    Example().run()
