import re
import sqlalchemy as sql
import time
from rich import print
import filekeys
from miscellaneous.statfunc import clear, hashpass, verify, console

eng = sql.create_engine(f"{filekeys.postgresqllink}", isolation_level="AUTOCOMMIT")
db = eng.connect()


def changeusername(username):
    clear()
    print(f"Your current username is {username}")
    while True:
        newusername = input("Enter your new username: ")

        # Validates username
        if newusername == username:
            print("[red]Your new username is the same as the current username. Please try again.[/red]")
            continue

        elif not re.match("^[a-zA-Z0-9]([._-](?![._-])|[a-zA-Z0-9]){3,18}[a-zA-Z0-9]$", newusername):
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
        elif len((db.execute(f"SELECT * FROM users WHERE Username = %s", (newusername,))).fetchall()) == 1:
            print("[yellow]Username already exists! Please try again.[/yellow]")
            continue
        break

    while True:
        choice = input("Confirm username change? (Y/N) ").strip().lower()
        if choice == "y":
            break
        elif choice == "n":
            return False, None
        else:
            print(f"[red]Invalid input.[/red]")
            continue

    with console.status("Updating username...", spinner="dots") as status:

        # Updates username
        db.execute("UPDATE users SET Username = %s WHERE Username = %s", newusername, username)
        db.execute("UPDATE musicsettings SET Username = %s WHERE Username = %s", newusername, username)
        status.update(f"[green]Your new username is {newusername}.[/green] Returning to previous screen...")
        time.sleep(1.5)
        return True, newusername


def changepassword(username):
    clear()
    user = db.execute("SELECT * FROM users WHERE username = %s", username).fetchall()[0]._asdict()
    salt = user["salt"]
    oldpassword = user["password"]

    # Prompts user for new password
    while True:
        newpassword = input("Enter your new password: ")

        # Validates password
        if verify(salt, newpassword) == oldpassword:
            print("[red]Your new password cannot be the same as the current password. Please try again.[/red]")
            continue
    
        elif not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,32})", newpassword):
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
        if repassword == newpassword:
            break
        else:
            print("[red]Passwords do not match![/red]")
            continue
    
    while True:
        choice = input("Confirm password change? (Y/N) ").strip().lower()
        if choice == "y":
            break
        elif choice == "n":
            return False
        else:
            print("[red]Invalid input.[/red]")
            continue
    with console.status("Updating password...", spinner="dots") as status:

        # Updates password
        salt, password = hashpass(newpassword)
        db.execute("UPDATE users SET password = %s, salt = %s WHERE username = %s", password, salt, username)
        status.update("[green]Password updated.[/green] Returning to previous screen...")
        time.sleep(1.5)
        return True


def changesearchresults(username, NUMSEARCHES):
        print(f"Your current setting shows you {NUMSEARCHES} searches on each page.")

        # Prompt the user to enter 
        while True:
            try:
                num = int(input("Enter the number of search results you wish to see in a page: "))
                if num > 0:
                    break
                else:
                    print("Number must be greater than 0")
                    continue
            except ValueError:
                print("[red]Please enter a number.[/red]")
                continue
        
        while True:
            choice = input("Confirm search results change? (Y/N) ").strip().lower()
            if choice == "y":
                break
            elif choice == "n":
                return False, None
            else:
                print(f"[red]Invalid input.[/red]")
                continue
        
        with console.status("Updating search results...", spinner="dots") as status:

            # Updates search results
            db.execute("UPDATE musicsettings SET numsearches = %s WHERE username = %s", num, username)
            status.update(f"[green]Number of search results changed to {num}.[/green] Returning to previous screen...")
            time.sleep(1.5)
            return True, num
