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

        # Show the "Copy to Clipboard" button
        button_copy.pack(pady=10)

        # Start the fade-in effect for both the label and button
        fade_in_label_and_button(0)

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

# Helper function to implement the fade-in effect on the label and button
def fade_in_label_and_button(count):
    if count < 100:
        # Convert count to a hex string for background color
        bg_color = f"#{count:02x}{count:02x}{count:02x}"  # Background from black to white
        
        # Adjust the text color based on the brightness of the background
        if count < 50:  # Dark background
            text_color = "white"
            button_text_color = "white"
        else:  # Light background
            text_color = "black"
            button_text_color = "black"
        
        # Update label result with the new colors
        label_result.configure(fg_color=bg_color, text_color=text_color)
        
        # Update hash password button with the new colors
        button_hash.configure(fg_color=bg_color, text_color=button_text_color)

        # Continue the fade effect
        label_result.after(10, fade_in_label_and_button, count + 1)

# Set up the main window
root = ctk.CTk()
root.title("Password Hasher v1.3")
root.geometry("850x350")  # Increase the window size to fit the long hashed password
root.resizable(False, False)  # Make the window non-resizable

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

# Copy to Clipboard Button (Initially hidden)
button_copy = ctk.CTkButton(frame, text="Copy to Clipboard", command=copy_to_clipboard)

# Global variable to store the current hashed password
current_hashed_password = ""

# Start the GUI
root.mainloop()
