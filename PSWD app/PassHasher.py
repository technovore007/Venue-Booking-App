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

        # Store the hashed password for clipboard functionality
        global current_hashed_password
        current_hashed_password = hashed_password

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        progress_bar.stop()


# Function to copy the hashed password to clipboard
def copy_to_clipboard():
    if current_hashed_password:
        root.clipboard_clear()  # Clear the clipboard
        root.clipboard_append(current_hashed_password)  # Append the hashed password
        messagebox.showinfo("Copied", "Hashed password copied to clipboard.")
    else:
        messagebox.showwarning("No Hash", "Please hash a password first.")


# Set up the main window
root = ctk.CTk()
root.title("Password Hasher")
root.geometry("400x350")

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
label_result = ctk.CTkLabel(frame, text="", font=("Cascadia Code", 16))

# Copy to Clipboard Button
button_copy = ctk.CTkButton(frame, text="Copy to Clipboard", command=copy_to_clipboard)
button_copy.pack(pady=10)

# Global variable to store the current hashed password
current_hashed_password = ""

# Start the GUI
root.mainloop()
