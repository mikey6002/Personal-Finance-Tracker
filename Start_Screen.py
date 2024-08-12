import os
import re
import csv
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.config import Config
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

# Enable the virtual keyboard
Config.set('kivy', 'keyboard_mode', 'multi')

class Start_Screen(MDApp):
    # Email verification regex
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # This is just creating that basic screen and then acknowledging the kivy files that I have.
    def build(self):
        screen_manager = ScreenManager()

        # Check and load KV files
        kv_files = ["main.kv", "login.kv", "Signup.kv", "Questionare.kv","UserInformation.kv",]
        for kv in kv_files:
            if os.path.exists(kv):
                loaded_widget = Builder.load_file(kv)
                if isinstance(loaded_widget, Screen):
                    screen_manager.add_widget(loaded_widget)
                    
                # Check and load Python files
        py_files = ["Questionare.py"]
        for py in py_files:
            if os.path.exists(py):
                module_name = os.path.splitext(py)[0]
                __import__(module_name)

        return screen_manager


    # This is the data grabber
    def send_data(self, email_field, password_field):
        email = email_field.text
        password = password_field.text
        if re.fullmatch(self.regex, email):
            with open('logindata.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([email, password])
            # Clear the text fields after saving
            email_field.text = ""
            password_field.text = ""
            
    def on_login_button_press(self, instance):
        self.recieve_data(self.email_field, self.password_field)

     # This is the data receiver, when you log in -> it checks to see if that email/password exists in the database
    def recieve_data(self, email_field, password_field):
        email = email_field.text
        password = password_field.text
        email_list = []
        with open('logindata.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                email_list.append(row[0])
                if email == row[0] and password == row[1]:
                    print("You have successfully logged in!")
                    # Dynamically load and execute the Python file
                    module_name = "Questionare"
                    if os.path.exists(f"{module_name}.py"):
                        module = __import__(module_name)
                        if hasattr(module, 'main'):
                            module.main()  # Call the main function or class from the module
                    # Change to the Questionare screen
                    self.root.current = "questionare"
                    return
        print("Invalid email or password")

    def submit_data(self):
        # Access the ids from the BudgetScreen (which is the "questionare" screen in this case)
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
            writer.writerow([income, monthly_bills, loans, entertainment, rent, groceries, insurance, misc, savings])

            self.show_confirmation_dialog()

            progress_bar = self.root.get_screen('questionare').ids.progress_bar
            progress_bar.opacity = 1
            progress_bar.value = 0
            Clock.schedule_interval(self.update_progress, 0.1)
    # message after clicking submit data
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
    # small progress bar 
    def update_progress(self, dt):
        progress_bar = self.root.get_screen('questionare').ids.progress_bar
        if progress_bar.value < 100:
            progress_bar.value += 10
        else:
            progress_bar.opacity = 0
            return False

if __name__ == '__main__':
    Start_Screen().run()