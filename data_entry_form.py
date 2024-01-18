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

        # Create form elements
        label_player_id = Label(self.master, text="Player ID:")
        label_player_id.grid(row=0, column=0)
        entry_player_id = Entry(self.master)
        entry_player_id.grid(row=0, column=1)

        label_player_name = Label(self.master, text="Player Name:")
        label_player_name.grid(row=1, column=0)
        entry_player_name = Entry(self.master)
        entry_player_name.grid(row=1, column=1)

        label_tournament_id = Label(self.master, text="Tournament Event")
        label_tournament_id.grid(row=2, column=0)
        entry_tournament_id = Entry(self.master)
        entry_tournament_id.grid(row=2, column=1)

        label_tournament_format = Label(self.master, text="Tournament Format")
        label_tournament_format.grid(row=3, column=0)
        tournament_format_options = ["Standard", "V-Premium", "Premium"]
        combo_tournament_format = ttk.Combobox(self.master, values=tournament_format_options)
        combo_tournament_format.grid(row=3, column=1)

        label_tournament_date = Label(self.master, text="Tournament Date")
        label_tournament_date.grid(row=4, column=0)
        entry_tournament_date = Entry(self.master)
        entry_tournament_date.grid(row=4, column=1)

        calendar_button = Button(self.master, text="Select Date", command=self.show_calendar)
        calendar_button.grid(row=4, column=2, columnspan=2)

        label_deck_nation = Label(self.master, text="Deck Nation")
        label_deck_nation.grid(row=5, column=0)
        entry_deck_nation = Entry(self.master)
        entry_deck_nation.grid(row=5, column=1)

        label_deck_clan = Label(self.master, text="Deck Clan (if not standard format)")
        label_deck_clan.grid(row=6, column=0)
        entry_deck_clan = Entry(self.master)
        entry_deck_clan.grid(row=6, column=1)

        label_deck_subclan = Label(self.master, text="Deck Subclan")
        label_deck_subclan.grid(row=7, column=0)
        entry_deck_subclan = Entry(self.master)
        entry_deck_subclan.grid(row=7, column=1)

        label_tournament_ranking = Label(self.master, text="Ranking from tournament")
        label_tournament_ranking.grid(row=8, column=0)
        entry_tournament_ranking = Entry(self.master)
        entry_tournament_ranking.grid(row=8, column=1)


        # Add more labels and entry fields
        #  as needed

        insert_button = Button(self.master, text="Submit", command=self.insert_data)
        insert_button.grid(row=9, column=0, columnspan=2)

    def show_calendar(self):
        top = tk.Toplevel(self.master)
        cal = DateEntry(top, width=12, background='darkblue', foreground='white', borderwidth=2, year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        cal.grid(row=0, column=0, padx=10, pady=10)
        select_button = Button(top, text="Select Date", command=self.on_date_selected)
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
        self.entry_deck_nation.delete(0, tk.END)
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
        deck_nation = self.entry_deck_nation.get()
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