from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import mysql.connector
import os
import re


class Slope(MDApp):
    #i found like this email verification thing 
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    #getting the database i created in the SQL environment by providing them with full access
    database = mysql.connector.Connect(host="localhost", user="root", password="Lovebug@1022", database="Loginform")
    cursor = database.cursor()
    cursor.execute("select * from logindata")
    for i in cursor.fetchall():
        print(i[0], i[1])
    
    #this is just creating that basic scren and then aknowledging the kivy files that i have. 
    def build(self):
        screen_manager = ScreenManager()

        # Check and load KV files
        kv_files = ["main.kv", "Login.kv", "Signup.kv", "dashboard.kv","UserInformation.kv"]
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
#this is the data grabber, 
    def send_data(self, email, password):
        #if re.fullmatch(self.regex, email.text):
            self.cursor.execute(f"INSERT INTO logindata (email, password) VALUES ('{email.text}', '{password.text}')")
            self.database.commit()
            #for i in self.cursor.fetchall():
                #print(i[0], i[1])
            #email.text=""
            #password.text=""

        #for i in self.cursor.fetchall():
            #print(i[0], i[1])

#this is the data reciever, when you log in-> it checks to see if that email/password exists in that database 
    def recieve_data(self, email, password):
        self.cursor.execute("select * from logindata")
        email_list=[]
        for i in self.cursor.fetchall():
            email_list.append(i[0])
        if email.text in email_list and email.text != "":
            self.cursor.execute(f"select password from logindata where email='{email.text}'")
            for j in self.cursor: 
                if password.text == j[0]:
                    print("You have successfully logged in!")
                    #i want this  to be on the  successfully logged in, go to the dashbored .kv page. 
                    self.root.transition.direction = "left"
                    self.root.current = "dashboard"
                else:
                    print("Incorrect Password")
        else: 
            print("Incorrect Email")


if __name__ == "__main__":
    Slope().run()