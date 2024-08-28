class MainApp(MDApp):
    def build(self):
        self.title = "Transactions"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        
        self.root = Builder.load_string(KV)
        
        csv_file_path = 'user_data.csv'  # path of file
        if not os.path.exists(csv_file_path):
            print(f"File {csv_file_path} not found.")
            return

        
        table_data = []

        # Open the CSV file and read the transactions
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            row = next(reader)  # Assuming only one row of data
            
            # Extract and format the transaction-related data dynamically
            for i in range(1, 11):  # For 10 transactions (t1 to t10)
                date_key = f"t{i}date"
                name_key = f"t{i}name"
                amount_key = f"t{i}amount"
                
                try:
                    date_str = row[date_key]
                    name = row[name_key]
                    amount = row[amount_key].replace('$', '').replace(',', '')  # Handle $ and commas
                    amount = float(amount)
                    table_data.append((date_str, name, f"${amount:.2f}"))
                except KeyError as e:
                    print(f"Error: Missing data for transaction {i}.")
                except ValueError as e:
                    print(f"Error: Incorrect value format for transaction {i} amount.")
    
        # Create DataTable with pagination enabled
        self.data_table = MDDataTable(
            size_hint=(1, None),
            height=dp(600),  # Increased height for the data table
            rows_num=10,  # Number of rows per page
            column_data=[
                ("Date", dp(13)),
                ("Name", dp(35)),
                ("Amount", dp(19)),
            ],
            row_data=table_data,
        )

        # Add the data table to the layout
        self.root.ids.data_table_box.add_widget(self.data_table)
        return self.root

    def categories_dropper(self):
        menu_items = [
            {"text": "Online Shopping", "on_release": lambda x="Online Shopping": self.menu_callback('categories', x)},
            {"text": "Dining", "on_release": lambda x="Dining": self.menu_callback('categories', x)},
            {"text": "Utilities", "on_release": lambda x="Utilities": self.menu_callback('categories', x)},
            {"text": "Gas & EV Charging", "on_release": lambda x="Gas & EV Charging": self.menu_callback('categories', x)},
        ]
        self.menu = MDDropdownMenu(
            caller=self.root.ids.categories,
            items=menu_items,
            width_mult=3
        )
        self.menu.open()

    def menu_callback(self, widget_id, text_item):
        self.root.ids[widget_id].text = text_item
        self.menu.dismiss()

MainApp().run()