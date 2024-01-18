import psycopg2
from tkinter import messagebox

class DatabaseOperations:
    DB_NAME = "Top Deck CFV"
    DB_USER = "postgres"
    DB_PASSWORD = "chromedokuro14"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    def connect(self):
        try:
            conn = psycopg2.connect(
                dbname=self.DB_NAME,
                user=self.DB_USER,
                password=self.DB_PASSWORD,
                host=self.DB_HOST,
                port=self.DB_PORT
            )
            return conn
        except psycopg2.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to the database: {e}")
            return None
        
    def insert_data(self, conn, player_id, player_name, tournament_event, tournament_format,
                    tournament_date, deck_nation, deck_clan, deck_subclan, tournament_ranking):
        with conn.cursor() as cursor:
            cursor.execute(
                """INSERT INTO players_statistics ( 
                    player_id,
                    player_name,
                    tournament_event,
                    tournament_format,
                    tournament_date,
                    deck_nation,
                    deck_clan,
                    deck_subclan,
                    tournament_ranking  
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (player_id, player_name, tournament_event, tournament_format,
                 tournament_date, deck_nation, deck_clan, deck_subclan, tournament_ranking)
            )
            conn.commit()