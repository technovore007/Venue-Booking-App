import bcrypt

password = input("Enter a password: ") # Example password
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
print("Hashed password:", hashed_password)
