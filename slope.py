from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import os

class SignupScreen(Screen):
    pass

class Slope(MDApp):
    def build(self):
        screen_manager = ScreenManager()

        # Check and load KV files
        kv_files = ["main.kv", "Login.kv", "Signup.kv"]
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

    def signer(self):
        if 'signup' not in self.root.ids:
            return
        
        welcome_label = self.root.ids.signup.ids.welcome_label
        welcome_label.text = f'Welcome in, {self.root.ids.signup.ids.username.text}'
        
        if self.root.ids.signup.ids.username.text.strip() == '' or \
           self.root.ids.signup.ids.email.text.strip() == '' or \
           self.root.ids.signup.ids.password.text.strip() == '' or \
           self.root.ids.signup.ids.repassword.text.strip() == '':
            message = "Please fill in all fields."
            popup = Popup(title="Pop Up Window", content=Label(text=message), size_hint=(None, None), size=(400, 200))
            popup.open()
        elif self.root.ids.signup.ids.password.text != self.root.ids.signup.ids.repassword.text:
            message = "Passwords do not match."
            pwdpopup = Popup(title="Pop Up Window", content=Label(text=message), size_hint=(None, None), size=(400, 200))
            pwdpopup.open()
        else:
            filename = self.root.ids.signup.ids.username.text + '.txt'
            try:
                with open(filename, 'w') as file:
                    file.write('Name: {}\n'.format(self.root.ids.signup.ids.username.text))
                    file.write('Email: {}\n'.format(self.root.ids.signup.ids.email.text))
                    file.write('Password: {}\n'.format(self.root.ids.signup.ids.password.text))
                message = "Account successfully created!"
                rgstrpopup = Popup(title="Pop Up Window", content=Label(text=message), size_hint=(None, None), size=(400, 200))
                rgstrpopup.open()
            except IOError as e:
                print(f"Error writing to file: {e}")
        
        self.root.ids.signup.ids.username.text = ''
        self.root.ids.signup.ids.email.text = ''
        self.root.ids.signup.ids.password.text = ''
        self.root.ids.signup.ids.repassword.text = ''

if __name__ == "__main__":
    Slope().run()
