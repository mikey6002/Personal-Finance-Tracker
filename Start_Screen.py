import os
import re
import csv
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.config import Config
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd_extensions.akivymd.uix.charts import AKPieChart
from kivy.metrics import dp

# Enable the virtual keyboard
Config.set('kivy', 'keyboard_mode', 'multi')

from kivy.core.window import Window
Window.size = (380, 640)

def read_csv_data(file_path):
    headers = []
    values = []

    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader, [])  # Read the first line as headers
            values = next(reader, [])   # Read the second line as values
            
            # Process the data into rows with categories and amounts
            formatted_rows = []
            for i in range(len(headers)):
                formatted_rows.append((headers[i], values[i]))

    except Exception as e:
        print(f"Error reading CSV file: {e}")

    return formatted_rows

class Start_Screen(MDApp):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def build(self):
        screen_manager = ScreenManager()

        # Load KV files
        kv_files = ["main.kv", "login.kv", "Signup.kv", "Questionare.kv", "UserInformation.kv", "Dash.kv"]
        for kv in kv_files:
            if os.path.exists(kv):
                loaded_widget = Builder.load_file(kv)
                if isinstance(loaded_widget, Screen):
                    screen_manager.add_widget(loaded_widget)

        return screen_manager
    #stores login information
    def send_data(self, email_field, password_field):
        email = email_field.text
        password = password_field.text
        if re.fullmatch(self.regex, email):
            with open('logindata.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([email, password])
            email_field.text = ""
            password_field.text = ""

    def on_login_button_press(self, email_field, password_field):
        self.recieve_data(email_field, password_field)
        
    #checks if login info is correct
    def recieve_data(self, email_field, password_field):
        email = email_field.text
        password = password_field.text
        with open('logindata.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if email == row[0] and password == row[1]:
                    print("You have successfully logged in!")

                    # Switch to the dashboard screen
                    self.root.current = "dashboard"

                    # Load and initialize the Dashboard after a short delay
                    Clock.schedule_once(lambda dt: self.load_dashboard_data(), 0.1)
                    return
        print("Invalid email or password")
    #loads the dashboard
    def load_dashboard_data(self, dt=None):
        print("Loading dashboard data...")
        csv_file_path = 'user_data.csv'
        if not os.path.exists(csv_file_path):
            print(f"File {csv_file_path} not found.")
            return

        # Read and process data from CSV
        rows = read_csv_data(csv_file_path)
        if rows:
            print(f"Rows: {rows}")
            self.populate_data_table(rows)
            self.populate_pie_chart(rows)
      #information for csv to the table      
    def populate_data_table(self, rows):
        print("Populating data table...")
        try:
            data_table = self.root.get_screen('dashboard').ids.data_table
            data_table.clear_widgets()  # Clear existing widgets
            
            # Create a new MDDataTable with the formatted data
            data_table.add_widget(MDDataTable(
                size_hint=(0.9, 0.9),
                use_pagination=True,
                check=True,
                column_data=[
                    ("Category", dp(40)),
                    ("Amount", dp(30)),
                ],
                row_data=rows
            ))
            print("Data table populated successfully.")
        except KeyError as e:
            print(f"Error accessing data table: {e}")
    #information for csv to the pie chart
    def populate_pie_chart(self, rows):
        print("Populating pie chart...")
        try:
            chart_box = self.root.get_screen('dashboard').ids.pie_chart
            chart_box.clear_widgets()  # Clear existing widgets

            # Calculate the total amount
            total_amount = sum(float(amount) for _, amount in rows)

            # Process the rows data into percentages
            chart_data = {}
            for category, amount in rows:
                percentage = (float(amount) / total_amount) * 100
                chart_data[category] = round(percentage, 1)  # Round to 1 decimal place

            # Ensure the sum is exactly 100%
            sum_percentages = sum(chart_data.values())
            if sum_percentages != 100:
                # Adjust the largest category to make the sum 100
                largest_category = max(chart_data, key=chart_data.get)
                chart_data[largest_category] += 100 - sum_percentages

            piechart = AKPieChart(
                items=[chart_data],
                pos_hint={"center_x": 0.7, "center_y": 0.5},
                size_hint=[None, None],
                size=(dp(300), dp(300)),
            )
            chart_box.add_widget(piechart)
            print("Pie chart populated successfully.")
            print(f"Chart data: {chart_data}")
        except KeyError as e:
            print(f"Error accessing pie chart: {e}")
        except ValueError as e:
            print(f"Error processing data: {e}")

if __name__ == '__main__':
    Start_Screen().run()
