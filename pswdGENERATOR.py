import bcrypt

password = "ehnd11"  # Example password
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
print("Hashed password:", hashed_password)
