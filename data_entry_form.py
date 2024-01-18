import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, ttk
from tkcalendar import Calendar, DateEntry
import psycopg2
from datetime import datetime

class DataCollectionApp:
    def __init__(self, master):
        self.master = master
        master.title("Data Collection Form")

        # Create form elements
        self.create_form_elements()

    def create_form_elements(self):
        form_elements_config = [
            {"label": "Player ID:", "type": Entry},
            {"label": "Player Name:", "type": Entry},
            {"label": "Tournament Event", "type": Entry},
            {"label": "Tournament Format", "type": ttk.Combobox, "values": ["Standard", "V-Premium", "Premium"]},
            {"label": "Tournament Date", "type": Entry},
            {"label": "Deck Nation", "type": ttk.Combobox, "values": ["Keter Sanctuary", "Dragon Empire", "Brandt Gate", "Dark States", "Stoicheia", "Lyrical Monasterio"]},
            {"label": "Deck Clan (if not standard format)", "type": Entry},
            {"label": "Deck Subclan", "type": Entry},
            {"label": "Ranking from tournament", "type": Entry},
        ]

        for i, element_config in enumerate(form_elements_config):
            label_text = element_config["label"]
            entry_type = element_config["type"]

            label = Label(self.master, text=label_text)
            label.grid(row=i, column=0)

            if entry_type == ttk.Combobox:
                values = element_config.get("values", [])
                entry = entry_type(self.master, values=values)
                if label_text == "Deck Nation":
                    self.combo_deck_nation = entry
            else:
                entry = entry_type(self.master)
            
            entry.grid(row=i, column=1)

        button_submit = Button(self.master, text="Submit", command=self.insert_data)
        button_submit.grid(row=len(form_elements_config), column=0, columnspan=2)

        self.combo_tournament_format = next((e["type"](self.master, values=e.get("values", [])) for e in form_elements_config if e["label"] == "Tournament Format"), None)
        if self.combo_tournament_format:
            self.combo_tournament_format.grid(row=form_elements_config.index(next(e for e in form_elements_config if e["label"] == "Tournament Format")), column=1)
            self.combo_tournament_format.bind("<<ComboboxSelected>>", self.update_second_dropdown)


    def update_second_dropdown(self, event=None):
        deck_nation_options = {
        "Standard": ["Keter Sanctuary", "Dragon Empire", "Brandt Gate", "Dark States", "Stoicheia", "Lyrical Monasterio"],
        "V-Premium": ["United Sanctuary", "Dragon Empire", "Star Gate", "Dark Zone", "Magallanica", "Zoo"],
        "Premium": ["United Sanctuary", "Dragon Empire", "Star Gate", "Dark Zone", "Magallanica", "Zoo"],
        }

        # Get the selected value from the first dropdown
        selected_value = self.combo_tournament_format.get()

        # Get the corresponding deck clan options from the dictionary
        deck_clan_options = deck_nation_options.get(selected_value, [])

        # Update the options of the second dropdown
        self.combo_deck_nation["values"] = deck_clan_options

    def show_calendar(self):
        self.top = tk.Toplevel(self.master)
        self.cal = DateEntry(self.top, width=12, background='darkblue', foreground='white', borderwidth=2, year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.cal.grid(row=0, column=0, padx=10, pady=10)
        select_button = Button(self.top, text="Select Date", command=self.on_date_selected)
        select_button.grid(row=1, column=0)

    def on_date_selected(self):
        date = self.cal.get_date()
        self.entry_tournament_date.delete(0, tk.END)
        self.entry_tournament_date.insert(0, date.strftime('%Y-%m-%d'))
        self.top.destroy()  # Close the calendar window after selecting a date

    def clear_form(self):
    # Clear all entry fields
        self.entry_player_id.delete(0, tk.END)
        self.entry_player_name.delete(0, tk.END)
        self.entry_tournament_id.delete(0, tk.END)
        self.combo_tournament_format.set("")  # Clear the selection in the combo box
        self.entry_tournament_date.delete(0, tk.END)
        self.combo_deck_nation.set("")
        self.entry_deck_clan.delete(0, tk.END)
        self.entry_deck_subclan.delete(0, tk.END)
        self.entry_tournament_ranking.delete(0, tk.END)

    def insert_data(self):
        # Get data from the GUI input fields
        player_id = self.entry_player_id.get()
        player_name = self.entry_player_name.get()
        tournament_id = self.entry_tournament_id.get()
        tournament_format = self.combo_tournament_format.get()
        tournament_date = self.entry_tournament_date.get()
        deck_nation = self.combo_deck_nation.get()
        deck_clan = self.entry_deck_clan.get()
        deck_subclan = self.entry_deck_subclan.get()
        tournament_ranking = self.entry_tournament_ranking.get()

        # Validate input (you can add more validation as needed)

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname="Top Deck CFV",
            user="postgres",
            password="chromedokuro14",
            host="localhost",
            port="5432"
        )

        # Check if a connection has been established
        if conn is None:
            messagebox.showerror("Error", "Database connection not established.")
            return

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        try:
            # Insert data into the table
            cursor.execute(
                """INSERT INTO players_statistics ( 
                    player_id,
                    player_name,
                    tournament_id,
                    tournament_format,
                    tournament_date,
                    deck_nation,
                    deck_clan,
                    deck_subclan,
                    tournament_ranking  
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (player_id, player_name, tournament_id, tournament_format, tournament_date, deck_nation, deck_clan, deck_subclan, tournament_ranking)
            )

            # Commit the transaction
            conn.commit()

            messagebox.showinfo("Success", "Data inserted successfully!")

            # Clear the form after successful submission
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")
            conn.rollback()
        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()

    def connect_to_database(self):
        try:
            # Connect to the PostgreSQL database
            conn = psycopg2.connect(
                dbname="Top Deck CFV",
                user="postgres",
                password="chromedokuro14",
                host="localhost",
                port="5432"
            )
            return conn
        except psycopg2.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to the database: {e}")
            return None