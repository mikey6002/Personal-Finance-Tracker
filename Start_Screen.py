import os
import csv
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.config import Config
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import matplotlib.pyplot as plt
from kivy.uix.image import Image
import io
import logging


# Enable the virtual keyboard
Config.set('kivy', 'keyboard_mode', 'multi')

# Global variable to store the logged-in user's email
current_user_email = None

class DashboardScreen(Screen):
    def on_enter(self):
        print(f"Entering DashboardScreen with current_user_email: {current_user_email}")
        if current_user_email is not None:
            self.display_dashboard()

    def display_dashboard(self):
        user_data = self.get_user_data(current_user_email)
        if user_data:
            print(f"Displaying data for user: {current_user_email}")
            print(f"User Data: {user_data}")

            # Update the labels with user data
            self.ids.income.text = f"Total Income: ${user_data.get('income', 'N/A')}"
            self.ids.groceries.text = f"Total Monthly Bills: ${user_data.get('groceries', 'N/A')}"
            self.ids.savings.text = f"Savings: ${user_data.get('savings', 'N/A')}"

            # Generate and display the graph
            self.generate_graph(user_data)

        else:
            print("No data found for the current user.")
            self.ids.income.text = "No data found."
            self.ids.groceries.text = "No data found."
            self.ids.savings.text = "No data found."

    def get_user_data(self, email):
        user_data = {}
        try:
            with open('user_data.csv', mode='r') as file:
                reader = csv.DictReader(file)
                headers = reader.fieldnames
                print(f"CSV Headers: {headers}")
                for row in reader:
                    print(f"CSV Row: {row}")
                    if row.get('email') == email:
                        user_data = row
                        break
        except FileNotFoundError:
            print("The CSV file was not found.")
        except KeyError as e:
            print(f"Key error: {e}")
        return user_data
    #supressing all the debug statments that makes my machine run slower.
    logging.getLogger('matplotlib').setLevel(logging.WARNING) 
    
    def generate_graph(self, user_data):
        labels = ['Income', 'Groceries', 'Savings']
        values = [
            float(user_data.get('income', 0)),
            float(user_data.get('groceries', 0)),
            float(user_data.get('savings', 0))
        ]

        plt.figure(figsize=(4, 3))
        plt.bar(labels, values, color=['blue', 'orange', 'green'])
        plt.title('Financial Overview')

        plt.savefig("graph.png")  # Save the graph as a PNG file
        plt.close()

        # Load the saved graph into Kivy
        graph_image = Image(source="graph.png")
        self.ids.graph_canvas.clear_widgets()
        self.ids.graph_canvas.add_widget(graph_image)

class Start_Screen(MDApp):
    # Email verification regex
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def build(self):
        screen_manager = ScreenManager()

        # Load KV files and add screens to the ScreenManager
        kv_files = ["main.kv", "login.kv", "Signup.kv", "Questionare.kv", "dashboard.kv"]
        for kv in kv_files:
            if os.path.exists(kv):
                loaded_widget = Builder.load_file(kv)
                if isinstance(loaded_widget, Screen):
                    screen_manager.add_widget(loaded_widget)
        
        # Add DashboardScreen to the ScreenManager
        if not screen_manager.has_screen('dashboard'):
            dashboard_screen = DashboardScreen(name='dashboard')  # Correct instantiation
            screen_manager.add_widget(dashboard_screen)

        return screen_manager

    def recieve_data(self, email_field, password_field):
        global current_user_email  # Access the global variable
        email = email_field.text
        password = password_field.text

        print(f"Attempting to log in with email: {email} and password: {password}")

        with open('user_data.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if email == row[0] and password == row[1]:
                    print("Login successful!")
                    current_user_email = email  # Store the logged-in user's email
                    print(f"current_user_email set to: {current_user_email}")
                    self.root.current = "dashboard"  # Switch to the dashboard screen
                    return
        print("Invalid email or password")

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

def prepare_pie_chart_data(user_data):
    data = {
        'Monthly Bills': float(user_data.get('monthly_bills', 0)),
        'Loans': float(user_data.get('loans', 0)),
        'Entertainment': float(user_data.get('entertainment', 0)),
        'Rent': float(user_data.get('rent', 0)),
        'Groceries': float(user_data.get('groceries', 0)),
        'Insurance': float(user_data.get('insurance', 0)),
        'Misc': float(user_data.get('misc', 0)),
    }
    return data

if __name__ == '__main__':
    Start_Screen().run()
