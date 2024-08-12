from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd_extensions.akivymd.uix.charts import AKPieChart
from kivymd.uix.datatables import MDDataTable

Window.fullscreen = False
Window.size = (380, 640)

class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class Example(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('Dash.kv')

    def on_start(self):
        self.items = [{"Python": 70, "Dart": 10, "C#": 10, "Css": 10}]
        self.piechart = AKPieChart(
            items=self.items,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=[None, None],
            size=(dp(150), dp(150)),
        )
        self.root.ids.chart_box.add_widget(self.piechart)

        # Create and add the datatable
        self.data_table = MDDataTable(
            size_hint=(None, None),
            size=(dp(300), dp(400)),  # Set the size directly here
            use_pagination=True,
            column_data=[
                ("Date", dp(20)),
                ("Description", dp(20)),
                ("Amount", dp(20)),
            ],
            row_data=[
                ("01/01", "Groceries", "$50"),
                ("01/02", "Gas", "$30"),
                ("01/03", "Restaurant", "$45"),
                # Add more rows as needed
            ],
        )
        self.root.ids.data_table_box.add_widget(self.data_table)

    def remove_chart(self):
        self.root.ids.chart_box.remove_widget(self.piechart)

if __name__ == '__main__':
    Example().run()