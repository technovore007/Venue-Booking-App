import tkinter as tk
import customtkinter as ctk
import bcrypt
from tkinter import messagebox


# Function to hash the password
def hash_password():
    password = entry_password.get()  # Get the password input
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password.")
        return

    # Start the animation
    progress_bar.start()

    try:
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # Stop the animation after hashing
        progress_bar.stop()

        # Display the hashed password using configure
        label_result.configure(text="Hashed password: " + hashed_password)
        label_result.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        progress_bar.stop()


# Set up the main window
root = ctk.CTk()
root.title("Password Hasher")
root.geometry("400x300")

# Set up a frame for better organization
frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, expand=True, fill='both')

# Title label
label_title = ctk.CTkLabel(frame, text="Password Hasher", font=("Arial", 18, "bold"))
label_title.pack(pady=10)

# Password entry
entry_password = ctk.CTkEntry(frame, placeholder_text="Enter your password", show="*")
entry_password.pack(pady=10, padx=10, fill="x")

# Hash button
button_hash = ctk.CTkButton(frame, text="Hash Password", command=hash_password)
button_hash.pack(pady=10)

# Progress bar (for animation while hashing)
progress_bar = ctk.CTkProgressBar(frame)
progress_bar.pack(pady=10, fill="x")

# Label to show the hashed password result
label_result = ctk.CTkLabel(frame, text="", font=("Arial", 10))

# Start the GUI
root.mainloop()
