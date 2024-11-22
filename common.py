import mysql.connector
from tkinter import messagebox

def connect_db():
    """Establish a connection to the MySQL database."""
    try:
        return mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="ehnd11", 
            database="venue_booking_system"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Connection Error", f"Unable to connect to the database: {err}")
        raise
