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
            file.write(f"Cardname:{cardname}\n")
            file.write(f"Cardnumber:{cardnumber}\n")
            file.write(f"Expiration date:{expirationdate}\n")
            file.write(f"Fico Score:{ficoscore}\n")
            file.write(f"Transaction 1 date:{tranaction1date}\n")
            file.write(f"Transaction 1 name:{transaction1name}\n")
            file.write(f"Transaction 1 ammount:{transaction1ammount}\n")
            file.write(f"Transaction 2 date:{tranaction2date}\n")
            file.write(f"Transaction 2 name:{transaction2name}\n")
            file.write(f"Transaction 2 ammount:{transaction2ammount}\n")
            file.write(f"Transaction 3 date:{tranaction3date}\n")
            file.write(f"Transaction 3 name:{transaction3name}\n")
            file.write(f"Transaction 3 ammount:{transaction3ammount}\n")
            file.write(f"Transaction 4 date:{tranaction4date}\n")
            file.write(f"Transaction 4 name:{transaction4name}\n")
            file.write(f"Transaction 4 ammount:{transaction4ammount}\n")
            file.write(f"Transaction 5 date:{tranaction5date}\n")
            file.write(f"Transaction 5 name:{transaction5name}\n")
            file.write(f"Transaction 5 ammount:{transaction5ammount}\n")

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
