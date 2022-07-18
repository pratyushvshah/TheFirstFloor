import os
import hashlib
import re
from datetime import datetime, timezone
import sqlalchemy as sql
from rich.console import Console
from rich import print
import time
import filekeys

# Configure console for using rich module
console = Console()

# Connects to database
eng = sql.create_engine(f"{filekeys.postgresqllink}", isolation_level="AUTOCOMMIT")
db = eng.connect()

# Secret keys
referralkey = filekeys.referralkey


# Login
def login():
    print("""
----------------------------------------------LOGIN------------------------------------------------
""")
    while True:
        username = input("Username: ")
        password = input("Password: ")
        print()

        # Retrieves the user's information from the database
        user = db.execute('SELECT * FROM users WHERE username = %s', username).all()

        # Checks if the user exists
        if user:
            user = user[0]._asdict()
            salt = user["salt"]
            with console.status("Verifying credentials...", spinner = "dots"):
                password = verify(salt, password)
                time.sleep(1.5)
            if password == user["password"]:
                with console.status("Logging in...", spinner = "dots"):

                    # Updates database to reflect when the user last logged in
                    db.execute("UPDATE users SET lastlogin = %s WHERE username = %s", datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), username)
                    time.sleep(1.5)
                return username
            else:
                print("[red]Invalid credentials[/red]")
                continue
        else:
            print("[red]User does not exist[/red]")
            continue


# Register
def create_user():
    print("""
---------------------------------------------REGISTER----------------------------------------------
""")

    # Asks user for a referral code
    while True:
        referral = input("Referral code: ")
        if not referral == referralkey:
            print("[red]Invalid referral code. Please try again.[/red]")
            continue
        else:
            break

    # Asks user for full name
    while True:
        fullname = input("Full name: ")
        choice = input("Is this correct? (Y/N): ").strip().upper()
        if choice == "Y":
            break
        elif choice == "N":
            continue
        else:
            msg = "Invalid input: " + choice
            return False, msg
    
    # Asks user for email
    while True:
        email = input("Email: ")
        if not re.match(r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""", email):
            print("[red]Invalid email address. Please try again.[/red]")
            continue
        choice = input("Is this correct? (Y/N): ").strip().upper()
        if choice == "Y":
            break
        elif choice == "N":
            continue
        else:
            msg = "Invalid input: " + choice
            return False, msg    

    # Prompts user for new username
    while True:
        username = input("Username: ")

        # Validates username
        if not re.match("^[a-zA-Z0-9]([._-](?![._-])|[a-zA-Z0-9]){3,18}[a-zA-Z0-9]$", username):
            print("""
[red]Invalid Username!
Username must follow the following criteria:
1. Username consists of alphanumeric characters (a-zA-Z0-9), lowercase, or uppercase.
2. Username allowed of the dot (.), underscore (_), and hyphen (-).
3. The dot (.), underscore (_), or hyphen (-) must not be the first or last character.
4. The dot (.), underscore (_), or hyphen (-) does not appear consecutively, e.g., java..regex
5. The number of characters must be between 5 to 20.[/red]
            """)
            continue

        # Checks if username already exists
        elif len((db.execute(f"SELECT * FROM users WHERE Username = %s", (username,))).fetchall()) == 1:
            print("[yellow]Username already exists! Please try again.[/yellow]")
            continue

        break

    # Prompts user for new password
    while True:
        password = input("Password: ")
    
        # Validates password
        if not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,32})", password):
            print("""
[red]Invalid Password!
Password must follow the following criteria:
1. At least one digit [0-9]
2. At least one lowercase character [a-z]
3. At least one uppercase character [A-Z]
4. At least one special character [!@#\$%\^&\*]
5. At least 8 characters in length, but no more than 32.)[/red]
            """)
            continue

        break
    
    # Prompts user for confirmation of new password
    while True:
        repassword = input("Confirm Password: ")
        if repassword == password:
            break
        else:
            print("[red]Passwords do not match![/red]")
            continue
    with console.status("Updating database", spinner = "dots"):
        salt, password = hashpass(password)
        updateCredentials(fullname, email, username, password, salt)
        msg = "Account created successfully! Please login to continue."
        time.sleep(1.5)
    return True, msg


# Create new user in database 
def updateCredentials(fullname, email, username, password, salt):

    db.execute("INSERT INTO users (fullname, email, username, password, salt) VALUES (%s, %s, %s, %s, %s)", fullname, email, username, password, salt)


# Creates hex of a password
def hashpass(password):

    # Generates a random salt
    salt = os.urandom(32).hex().encode()

    # Convert password to byte 
    plaintext = password.encode()

    # Hash the password
    hash = hashlib.pbkdf2_hmac('sha512', plaintext, salt, 500000)

    # Return the salt and the hashed password
    return salt.decode(), hash.hex()


# Returns hex of the inputted password
def verify(salt, password):

    # Convert password and salt to byte
    plaintext = password.encode()
    salt = salt.encode()

    # Hash the password
    hash = hashlib.pbkdf2_hmac('sha512', plaintext, salt, 500000)

    # Return the hashed password
    return hash.hex()
