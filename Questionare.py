from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

class BudgetScreen(Screen):
    pass

class MainApp(MDApp):
    def build(self):
        return Builder.load_file('Questionare.kv')

    def submit_data(self):
        # Access the ids from the BudgetScreen
        income = self.root.get_screen('questionare').ids.income.text
        monthly_bills = self.root.get_screen('questionare').ids.bills.text
        loans = self.root.get_screen('questionare').ids.loans.text
        entertainment = self.root.get_screen('questionare').ids.entertainment.text
        rent = self.root.get_screen('questionare').ids.rent.text
        groceries = self.root.get_screen('questionare').ids.groceries.text
        insurance = self.root.get_screen('questionare').ids.insurance.text
        savings = self.root.get_screen('questionare').ids.savings.text
        misc = self.root.get_screen('questionare').ids.misc.text
        
        # Write the data to a file
        with open("user_data.txt", "w") as file:
            file.write(f"Income: {income}\n")
            file.write(f"Monthly bills: {monthly_bills}\n")
            file.write(f"Loans: {loans}\n")
            file.write(f"Entertainment: {entertainment}\n")
            file.write(f"Rent: {rent}\n")
            file.write(f"Groceries: {groceries}\n")
            file.write(f"Insurance: {insurance}\n")
            file.write(f"Savings: {savings}\n")
            file.write(f"Misc: {misc}\n")

        # Show a confirmation dialog
        self.show_confirmation_dialog()

        # Start the progress bar
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

    def update_progress(self, dt):
        progress_bar = self.root.get_screen('questionare').ids.progress_bar
        if progress_bar.value < 100:
            progress_bar.value += 10
        else:
            progress_bar.opacity = 0
            return False

if __name__ == '__main__':
    MainApp().run()
