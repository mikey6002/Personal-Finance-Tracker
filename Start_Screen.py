import os
import re
import csv
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.config import Config

# Enable the virtual keyboard
Config.set('kivy', 'keyboard_mode', 'multi')

class Start_Screen(MDApp):
    # Email verification regex
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # This is just creating that basic screen and then acknowledging the kivy files that I have.
    def build(self):
        screen_manager = ScreenManager()

        # Check and load KV files
        kv_files = ["main.kv", "login.kv", "Signup.kv", "dashboard.kv","UserInformation.kv",]
        for kv in kv_files:
            if os.path.exists(kv):
                loaded_widget = Builder.load_file(kv)
                if isinstance(loaded_widget, Screen):
                    screen_manager.add_widget(loaded_widget)
                else:
                    print(f"Error: {kv} does not define a Screen widget.")
            else:
                print(f"Error: {kv} file not found.")

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
                    # Transition to the dashboard screen
                    self.root.transition.direction = "left"
                    self.root.current = "dashboard"
                    return
        print("Invalid email or password")

# Run the app
if __name__ == '__main__':
    Start_Screen().run()