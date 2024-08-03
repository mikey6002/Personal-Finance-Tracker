from kivy.lang import Builder
from kivymd.app import MDApp 
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class MainApp(MDApp):


    def build(self):
        self.title = "Sign Up"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "LightBlue"
        return Builder.load_file('login.kv')
    
    def signer(self):
        # This line write the user's name and says welcome
        self.root.ids.welcome_label.text = f'Welcome in, {self.root.ids.username.text}'
        #Every Field Required
        if self.root.ids.username.text.strip() == '' or self.root.ids.email.text.strip() == '' or self.root.ids.password.text.strip() == '' or self.root.ids.repassword.text.strip() == '':
            message = "Please fill in all fields."
            popup = Popup(title = "Pop Up Window", content = Label(text=message),size_hint=(None,None),size = (400,200))
            popup.open()
        elif self.root.ids.password.text != self.root.ids.repassword.text:
            message = "Passwords do not match."
            pwdpopup = Popup(title = "Pop Up Window", content = Label(text=message),size_hint=(None,None),size = (400,200))
            pwdpopup.open()
        else:
            filename = self.root.ids.username.text + '.txt'
            with open(filename, 'w') as file:
                file.write('Name: {}\n'.format(self.root.ids.username.text))
                file.write('Email: {}\n'.format(self.root.ids.email.text))
                file.write('Password: {}\n'.format(self.root.ids.password.text))
            print("Username: ", self.root.ids.username.text, 
                  "Email: ", self.root.ids.email.text, 
                  "Password: ", self.root.ids.password.text,
                  "Re-typed Password: ", self.root.ids.repassword.text)
            message = "Account successfully created!"
            rgstrpopup = Popup(title = "Pop Up Window", content = Label(text=message),size_hint=(None,None),size = (400,200))
            rgstrpopup.open()
        self.root.ids.username.text = ''
        self.root.ids.email.text = ''
        self.root.ids.password.text = ''
        self.root.ids.repassword.text = ''

        
        

    
MainApp().run()