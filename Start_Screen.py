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
from kivymd_extensions.akivymd.uix.charts import AKPieChart,AKBarChart
from kivy.metrics import dp
from decimal import Decimal, ROUND_HALF_UP
import webbrowser
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.app import App
from kivymd.uix.list import OneLineListItem

# Enable the virtual keyboard
Config.set('kivy', 'keyboard_mode', 'multi')

from kivy.core.window import Window
Window.size = (380, 740)

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

    def change_password(self, current_password, new_password, confirm_password):
        global current_user_email

        if current_password == "" or new_password == "" or confirm_password == "":
            self.show_dialog("Error", "All fields are required.")
            return

        if new_password != confirm_password:
            self.show_dialog("Error", "New passwords do not match.")
            return

        try:
            user_data = []
            password_updated = False

            with open('user_data.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == current_user_email and row[1] == current_password:
                        row[1] = new_password
                        password_updated = True
                    user_data.append(row)

            if password_updated:
                with open('user_data.csv', mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(user_data)
                self.show_dialog("Success", "Password changed successfully.")

            # Navigate back to the login screen
                self.root.current = 'login'
            else:
                self.show_dialog("Error", "Incorrect current password.")

        except Exception as e:
            print(f"Error while updating password: {e}")
            self.show_dialog("Error", "An error occurred while updating the password.")

    def show_dialog(self, title, text):
        if not hasattr(self, '_dialog'):
            self._dialog = None
    
        if self._dialog:
            self._dialog.dismiss()

        self._dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self._dialog.dismiss()
                )
            ],
        )
        self._dialog.open()
    
    def build(self):
        screen_manager = ScreenManager()

        # Load KV files
        kv_files = ["main.kv", "login.kv", "Signup.kv", "Questionare.kv", "UserInformation.kv", "Dash.kv", "rickroll.kv", "settings.kv", "passwordchange.kv","budget.kv", "transactions.kv"]
        for kv in kv_files:
            if os.path.exists(kv):
                loaded_widget = Builder.load_file(kv)
                if isinstance(loaded_widget, Screen):
                    screen_manager.add_widget(loaded_widget)

        return screen_manager
    
    def show_budget_screen(self):
        # Transition to the BudgetScreen
        self.root.current = "budget"
        self.show_top_5_categories()

    def open_youtube_link(self):
        webbrowser.open("https://youtu.be/dQw4w9WgXcQ?si=Obf1FUsbZsDX8-Ls")

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
        cardname = self.root.get_screen('questionare').ids.cardname.text
        cardnumber = self.root.get_screen('questionare').ids.cardnumber.text
        expirationdate = self.root.get_screen('questionare').ids.expirationdate.text
        ficoscore = self.root.get_screen('questionare').ids.ficoscore.text
        tranaction1date = self.root.get_screen('questionare').ids.tranaction1date.text
        transaction1name = self.root.get_screen('questionare').ids.transaction1name.text
        transaction1ammount = self.root.get_screen('questionare').ids.transaction1ammount.text
        tranaction2date = self.root.get_screen('questionare').ids.tranaction2date.text
        transaction2name = self.root.get_screen('questionare').ids.transaction2name.text
        transaction2ammount = self.root.get_screen('questionare').ids.transaction2ammount.text
        tranaction3date = self.root.get_screen('questionare').ids.tranaction3date.text
        transaction3name = self.root.get_screen('questionare').ids.transaction3name.text
        transaction3ammount = self.root.get_screen('questionare').ids.transaction3ammount.text
        tranaction4date = self.root.get_screen('questionare').ids.tranaction4date.text
        transaction4name = self.root.get_screen('questionare').ids.transaction4name.text
        transaction4ammount = self.root.get_screen('questionare').ids.transaction4ammount.text
        tranaction5date = self.root.get_screen('questionare').ids.tranaction5date.text
        transaction5name = self.root.get_screen('questionare').ids.transaction5name.text
        transaction5ammount = self.root.get_screen('questionare').ids.transaction5ammount.text

        # Save data as a CSV file
        with open("user_data.csv", mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([email, password, income, monthly_bills, loans, entertainment, rent, groceries, insurance, misc, savings, cardname, cardnumber, expirationdate, ficoscore, tranaction1date, transaction1name, transaction1ammount, tranaction2date, transaction2name, transaction2ammount, tranaction3date, transaction3name, transaction3ammount, tranaction4date, transaction4name, transaction4ammount, tranaction5date, transaction5name, transaction5ammount])

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
                    ("Date", dp(35)),
                    ("Name", dp(35)),
                    ("Amount", dp(30)),
                ],
                row_data=rows
            ))
            print("Data table populated successfully.")
        except KeyError as e:
            print(f"Error accessing data table: {e}")
            
    def on_start(self):
        # Call this function when the app starts
        self.populate_transactions_table()

    def populate_transactions_table(self):
        csv_file_path = 'user_data.csv'  # Update the path to your CSV file
        if not os.path.exists(csv_file_path):
            print(f"File {csv_file_path} not found.")
            return

        table_data = []

        # Open the CSV file and read the transactions
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            row = next(reader)  # Assuming only one row of data

            for i in range(1, 6):  # For 10 transactions (t1 to t10)
                date_key = f"t{i}date"
                name_key = f"t{i}name"
                amount_key = f"t{i}amount"

                try:
                    date_str = row[date_key]
                    name = row[name_key]
                    amount = row[amount_key].replace('$', '').replace(',', '')  # Handle $ and commas
                    amount = float(amount)
                    table_data.append((date_str, name, f"${amount:.2f}"))
                except KeyError as e:
                    print(f"Error: Missing data for transaction {i}.")
                except ValueError as e:
                    print(f"Error: Incorrect value format for transaction {i} amount.")

        if table_data:
                transactions_table = MDDataTable(
                    size_hint=(1, 1),
                    use_pagination=True,
                    check=False,
                    column_data=[
                        ("Transaction Date", dp(30)),
                        ("Description", dp(40)),
                        ("Amount", dp(30)),
                    ],
                    row_data=table_data,
                )

        
            # Access the transactions screen and the data_table_box layout
        transactions_screen = self.root.get_screen('transactions')
        data_table_box = transactions_screen.ids.data_table_box

        data_table_box.add_widget(transactions_table)




        


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


    def sign_out(self):
        # Logic for signing out (e.g., clearing current_user_email)
        global current_user_email
        current_user_email = None
        self.root.current = "login"  # Navigate back to the login screen

    def leave_application(self):
        # Logic for exiting the app
        App.get_running_app().stop()
        Window.close()
        
    #Start of budget screen code
    #same as reading files and ignores email password and savings        
    def show_budget_goals(self):
        self.root.current = "budget"
        self.show_top_5_categories()  # Call show_top_5_categories here
        
        csv_file_path = 'user_data.csv'
        if not os.path.exists(csv_file_path):
            print(f"File {csv_file_path} not found.")
            return

        bar_chart_data = []
        total_expense = 0
        try:
            with open(csv_file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['email'] == current_user_email:
                        for key, value in row.items():
                            if key not in ["email", "password", "savings","income"] and value and value.replace('.', '').isdigit():
                                amount = float(value)
                                bar_chart_data.append({
                                    'category': key,
                                    'value': amount
                                })
                                total_expense += amount
                        break
            # Sort the data by value in descending order
            bar_chart_data.sort(key=lambda x: x['value'], reverse=True)
        except Exception as e:
            print(f"Error reading CSV file: {e}")

        # Update the total expense label
        budget_screen = self.root.get_screen('budget')
        budget_screen.ids.total_expenseasd.text = f"Total expense is: ${total_expense:.2f}"

        # Update the bar chart
        self.update_bar_chart(bar_chart_data)

    # renders the bar chart
    def update_bar_chart(self, items):
        budget_screen = self.root.get_screen('budget')
        budget_screen.ids.bar_chart_box.clear_widgets()
        
        try:
            categories = []
            values = []
            x_values = []
            
            for index, item in enumerate(items, start=1):
                if 'category' in item and 'value' in item:
                    try:
                        value = float(item['value'])
                        if value > 0:
                            categories.append(item['category'])
                            values.append(value)
                            x_values.append(index)  # Use numeric index as x-value
                            print(f"Added category: {item['category']}, value: {value}")
                    except ValueError:
                        print(f"Skipping invalid value: {item['value']}")
            
            if not categories or not values:
                print("No valid data available for the bar chart.")
                return
            
            print(f"Categories: {categories}")
            print(f"Values: {values}")
            print(f"X-values: {x_values}")
            
            bar_chart = AKBarChart(
                x_values=x_values,
                y_values=values,
                x_labels=categories,  # Use categories as labels
                size_hint=(1, 1),
                size=(dp(300), dp(300)),
                labels=True,
                anim=True,
                label_size=9.3,
                bars_spacing=20
            )
            
            budget_screen.ids.bar_chart_box.add_widget(bar_chart)
            print("Bar chart populated successfully.")
        except Exception as e:
            print(f"Error in update_bar_chart: {e}")
            import traceback
            traceback.print_exc()
            
            
    def show_top_5_categories(self):
        print("show_top_5_categories function called")
        data = read_csv_data('user_data.csv', current_user_email)
        
        if data:
            print("Data retrieved:", data)  # Debug: Check retrieved data
            sorted_data = sorted(data, key=lambda x: Decimal(x[1]), reverse=True)
            top_5 = sorted_data[:5]
            
            print("Top 5 categories:", top_5)  # Debug: Check top 5 categories
            
            category_list = self.root.get_screen('budget').ids.category_list
            category_list.clear_widgets()
            
            for category, amount in top_5:
                item = OneLineListItem(text=f"{category}: {amount}")
                category_list.add_widget(item)
        else:
            print("No data found for user.")

            

if __name__ == '__main__':
    Start_Screen().run()