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
from kivy.uix.label import Label
from decimal import Decimal, ROUND_HALF_UP

# Enable the virtual keyboard
Config.set('kivy', 'keyboard_mode', 'multi')

from kivy.core.window import Window
Window.size = (380, 640)

current_user_email = None
def read_csv_data(file_path, user_email):
    headers = []
    values = []

    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['email'] == user_email:
                    headers = list(row.keys())
                    values = list(row.values())
                    break

            # Process the data into rows with categories and amounts
            formatted_rows = []
            for i in range(2, len(headers)):  # Skip 'email' and 'password' columns
                category = headers[i]
                amount = values[i]
                if amount:  # Ensure amount is not empty
                    formatted_rows.append((category, amount))

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

    def send_data(self, email_field, password_field):
        email = email_field.text
        password = password_field.text
        if re.fullmatch(self.regex, email):
            with open('user_data.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([email, password])
            email_field.text = ""
            password_field.text = ""
            
    def submit_data(self):
        # Access the ids from the BudgetScreen (which is the "questionare" screen in this case)
        email = self.root.get_screen('signup').ids.email.text
        password = self.root.get_screen('signup').ids.password.text
        income = self.root.get_screen('questionare').ids.income.text
        monthly_bills = self.root.get_screen('questionare').ids.bills.text
        loans = self.root.get_screen('questionare').ids.loans.text
        entertainment = self.root.get_screen('questionare').ids.entertainment.text
        rent = self.root.get_screen('questionare').ids.rent.text
        groceries = self.root.get_screen('questionare').ids.groceries.text
        insurance = self.root.get_screen('questionare').ids.insurance.text
        savings = self.root.get_screen('questionare').ids.savings.text
        misc = self.root.get_screen('questionare').ids.misc.text

        # Save data as a CSV file
        with open("user_data.csv", mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([email, password, income, monthly_bills, loans, entertainment, rent, groceries, insurance, misc, savings])

            self.show_confirmation_dialog()

            progress_bar = self.root.get_screen('questionare').ids.progress_bar
            progress_bar.opacity = 1
            progress_bar.value = 0
            Clock.schedule_interval(self.update_progress, 0.1)

    def show_confirmation_dialog(self):
        self.dialog = MDDialog(
            text="Your information has been saved successfully.",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.close_dialog
                )
            ],
        )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()
        self.root.current = "dashboard"
    
    def close_dialog(self, *args):
        self.dialog.dismiss()
        self.root.current = "login"
    
    def close_dialog(self, *args):
        self.dialog.dismiss()
        self.root.current = "login"

    def update_progress(self, dt):
        progress_bar = self.root.get_screen('questionare').ids.progress_bar
        if progress_bar.value < 100:
            progress_bar.value += 10
        else:
            progress_bar.opacity = 0
            return False
    

    def get_user_data_from_csv(email):
        user_data = {}
        try:
            with open('user_data.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row.get('email') == email:
                        user_data = row
                        break
        except FileNotFoundError:
            print("The CSV file was not found.")
        return user_data
    

    def on_login_button_press(self, email_field, password_field):
        self.recieve_data(email_field, password_field)
        
    def recieve_data(self, email_field, password_field):
        global current_user_email
        email = email_field.text
        password = password_field.text

        print(f"Attempting to log in with email: {email} and password: {password}")

        with open('user_data.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if email == row[0] and password == row[1]:
                    print("Login successful!")
                    current_user_email = email
                    print(f"current_user_email set to: {current_user_email}")
                    self.root.current = "dashboard"
                    Clock.schedule_once(self.load_dashboard_data, 0.1)
                    return
        print("Invalid email or password")

    def load_dashboard_data(self, dt=None):
        print("Loading dashboard data...")
        if current_user_email is None:
            print("No user logged in.")
            return

        csv_file_path = 'user_data.csv'
        if not os.path.exists(csv_file_path):
            print(f"File {csv_file_path} not found.")
            return

        rows = read_csv_data(csv_file_path, current_user_email)
        if rows:
            print(f"Rows for {current_user_email}: {rows}")
            self.populate_data_table(rows)
            self.populate_pie_chart(rows)

    def populate_data_table(self, rows):
        print("Populating data table...")
        try:
            data_table = self.root.get_screen('dashboard').ids.data_table
            data_table.clear_widgets()

            data_table.add_widget(MDDataTable(
                size_hint=(0.9, 0.9),
                use_pagination=True,
                check=True,
                column_data=[
                    ("Category", dp(35)),
                    ("Amount", dp(30)),
                ],
                row_data=rows
            ))
            print("Data table populated successfully.")
        except KeyError as e:
            print(f"Error accessing data table: {e}")
            



    def populate_pie_chart(self, rows):
        print("Populating pie chart...")
        try:
            chart_box = self.root.get_screen('dashboard').ids.pie_chart
            chart_box.clear_widgets()

            # Calculate total amount from financial data
            total_amount = sum(Decimal(amount) for _, amount in rows if amount and amount.replace('.', '').isdigit())

            chart_data = {}
            for category, amount in rows:
                if amount and amount.replace('.', '').isdigit():
                    value = Decimal(amount)
                    if value > 0:
                        percentage = (value / total_amount) * 100
                        chart_data[category] = percentage

            # Sort categories by percentage
            sorted_items = sorted(chart_data.items(), key=lambda x: x[1], reverse=True)

            # Take top 5 categories and group the rest as "Other"
            top_categories = sorted_items[:5]
            other_percentage = sum(item[1] for item in sorted_items[5:])

            rounded_data = {}
            remaining = Decimal('100')

            for category, percentage in top_categories:
                rounded_value = int(percentage.quantize(Decimal('1'), rounding=ROUND_HALF_UP))
                if rounded_value > 0:
                    rounded_data[category] = rounded_value
                    remaining -= Decimal(str(rounded_value))

            # Add "Other" category if it's significant
            if other_percentage >= 1:
                other_value = int(remaining)
                if other_value > 0:
                    rounded_data["Other"] = other_value
            else:
                # Distribute remaining to existing categories
                for category in list(rounded_data.keys()):
                    if remaining > 0:
                        rounded_data[category] += 1
                        remaining -= 1
                    else:
                        break

            # Ensure we have at least two categories for the pie chart
            if len(rounded_data) < 2:
                print("Not enough significant categories for a pie chart")
                return

            piechart = AKPieChart(
                items=[rounded_data],
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=[None, None],
                size=(dp(300), dp(300)),
            )
            chart_box.add_widget(piechart)
            print("Pie chart populated successfully.")
            print(f"Chart data: {rounded_data}")
            print(f"Sum of percentages: {sum(rounded_data.values())}")
        except Exception as e:
            print(f"Error in populate_pie_chart: {e}")

if __name__ == '__main__':
    Start_Screen().run()
