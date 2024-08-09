from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from kivy.core.window import Window
Window.fullscreen = False
Window.size = (380, 640)

class BudgetScreen(Screen):
    pass

class MainApp(MDApp):
    def build(self):
        return Builder.load_file('budget.kv')

    def submit_data(self):
        income = self.root.get_screen('budget').ids.income.text
        monthly_bills = self.root.get_screen('budget').ids.bills.text
        loans = self.root.get_screen('budget').ids.loans.text
        entertainment = self.root.get_screen('budget').ids.entertainment.text
        rent = self.root.get_screen('budget').ids.rent.text
        groceries = self.root.get_screen('budget').ids.groceries.text
        insurance = self.root.get_screen('budget').ids.insurance.text
        savings = self.root.get_screen('budget').ids.savings.text
        misc = self.root.get_screen('budget').ids.misc.text
    
        
        
        with open("user_data.txt", "w") as file:
            file.write(f"Income: {income}\n")
            file.write(f"monthy bill: {monthly_bills}\n")
            file.write(f"Loans: {loans}\n")
            file.write(f"Entertainment: {entertainment}\n")
            file.write(f"rent: {rent}\n")
            file.write(f"groceries: {groceries}\n")
            file.write(f"insurance: {insurance}\n")
            file.write(f"misc: {misc}\n")
            file.write(f"Savings: {savings}\n")
            
        
        self.show_confirmation_dialog()

        progress_bar = self.root.get_screen('budget').ids.progress_bar
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

    def update_progress(self, dt):
        progress_bar = self.root.get_screen('budget').ids.progress_bar
        if progress_bar.value < 100:
            progress_bar.value += 10
        else:
            progress_bar.opacity = 0
            return False

if __name__ == '__main__':
    MainApp().run()
