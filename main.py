from kivy.lang import Builder
from kivymd.app import MDApp 
from kivymd.uix.selectioncontrol import MDCheckbox

class MainApp(MDApp):


    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "LightBlue"
        return Builder.load_file('login.kv')
    def signer(self):
        self.root.ids.welcome_label.text = f'Welcome in, {self.root.ids.username.text}'
        print("Username: ", self.root.ids.username.text, "Email: ", self.root.ids.email.text, "Password: ", self.root.ids.password.text, "Re-typed Password: ", self.root.ids.repassword.text)
        self.root.ids.username.text = ""
        self.root.ids.email.text = ""
        self.root.ids.password.text = ''
        self.root.ids.repassword.text = ''

MainApp().run()