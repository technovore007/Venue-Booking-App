import customtkinter as ctk
from tkinter import messagebox

class UserConsole(ctk.CTk):
    def __init__(self, user):
        super().__init__()
        self.geometry("600x600")
        self.title("User Console")
        self.resizable(False, False)

        self.user = user
        self.setup_ui()

    def setup_ui(self):
        # Header Section
        header_frame = ctk.CTkFrame(self, height=50, fg_color="gray")
        header_frame.pack(side="top", fill="x")

        user_button = ctk.CTkButton(header_frame, text=self.user['username'], command=self.user_options)
        user_button.pack(side="left", padx=10, pady=10)

        burger_button = ctk.CTkButton(header_frame, text="☰", command=self.show_sidebar)
        burger_button.pack(side="right", padx=10, pady=10)

        # Current Bookings Section
        current_bookings_frame = ctk.CTkFrame(self, fg_color="gray")
        current_bookings_frame.pack(expand=True, fill="both", pady=20, padx=20)

        current_label = ctk.CTkLabel(current_bookings_frame, text="Current Bookings", font=("Arial", 18))
        current_label.pack(pady=10)

        self.current_bookings_list = ctk.CTkLabel(current_bookings_frame, text="No records found", font=("Arial", 14))
        self.current_bookings_list.pack()

        # Add Booking Button
        add_button = ctk.CTkButton(self, text="+", width=50, height=50, command=self.add_booking)
        add_button.place(relx=0.9, rely=0.9, anchor="center")

    def user_options(self):
        option = messagebox.askquestion("User Options", "Do you want to log out?")
        if option == "yes":
            self.destroy()
            from login_page import LoginPage
            LoginPage().mainloop()

    def show_sidebar(self):
        messagebox.showinfo("Past Bookings", "Sidebar functionality coming soon!")

    def add_booking(self):
        messagebox.showinfo("New Booking", "Booking flow coming soon!")

if __name__ == "__main__":
    # Example User Dictionary for Testing
    example_user = {'user_id': 'user123', 'username': 'John Doe', 'role': 'user'}
    app = UserConsole(example_user)
    app.mainloop()
