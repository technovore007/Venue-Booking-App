import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import bcrypt

# Database Connection Setup
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ehnd11',
    'database': 'venue_booking_system'
}

# Login Page Class
class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("Login Page")
        self.resizable(False, False)

        # UI Elements
        self.label = ctk.CTkLabel(self, text="JUIT Venue Booking System", font=("Arial", 20))
        self.label.pack(pady=20)

        self.user_id_label = ctk.CTkLabel(self, text="User ID:")
        self.user_id_label.pack(pady=5)
        self.user_id_entry = ctk.CTkEntry(self, width=200)
        self.user_id_entry.pack(pady=5)

        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self, width=200, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady=20)

    def login(self):
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()

        if not user_id or not password:
            messagebox.showwarning("Validation Error", "Please fill all fields!")
            return

        try:
            # Database Query
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT user_id, role, pswd FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            connection.close()

            # Debugging Output
            print(user)  # Remove this line after debugging

            if not user:
                messagebox.showerror("Error", "Invalid User ID or Password!")
                return

            # Check for 'pswd' Key
            if 'pswd' not in user:
                messagebox.showerror("Error", "Password data missing for this user!")
                return

            # Verify Password
            if bcrypt.checkpw(password.encode(), user['pswd'].encode()):
                if user['role'] == 'user':
                    self.destroy()
                    from user_console import UserConsole
                    UserConsole(user).mainloop()
                else:
                    messagebox.showinfo("Redirect", "Admin console is under construction!")
            else:
                messagebox.showerror("Error", "Invalid User ID or Password!")

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")


if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()
