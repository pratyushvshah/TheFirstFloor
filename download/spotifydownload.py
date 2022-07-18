import subprocess
import os
import re
import time
from datetime import datetime
from dateutil import tz
from spotdl.utils.spotify import SpotifyClient
from spotdl.utils.search import get_search_results
from rich.table import Table
from rich import print
import filekeys
from miscellaneous.statfunc import clear, console


# Connects to spotify
SpotifyClient.init(client_id=filekeys.spotclientid, client_secret=filekeys.spotsecretid)


# Convert seconds to hours, minutes and seconds
def seconds(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


# Special convert function to adhere with folder name requirements
def convert_time(time):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = datetime.strptime(time, '%Y-%m-%d %H.%M.%S')
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    return central.strftime('%Y-%m-%d %H.%M.%S')


# Searches for the song
def spotsearch():
    while True:
        query = input("Enter the name of the song you want to search for: ")
        if query == "":
            print("[red]Search can't be blank.[/red]")
            continue
        break
    try:
        with console.status("Searching for song...", spinner="dots") as status:
            result = get_search_results(query)
            if len(result) == 0:
                print("[red]No results found. Redirecting to previous screen...[/red]")
                time.sleep(1.5)
                return False
            status.update(f"Found {len(result)} results. Gathering data...")
            name = []
            artist = []
            album = []
            duration = []
            date = []
            link = []
            for i in range(len(result)):
                name.append(result[i].__getattribute__("name"))
                temp = result[i].__getattribute__("artists")
                artists = ""
                for j in range(len(temp)):
                    if j == 0:
                        artists += temp[j]
                    else:
                        artists += ", " + temp[j]
                artist.append(artists)
                album.append(result[i].__getattribute__("album_name"))
                duration.append(seconds(result[i].__getattribute__("duration")))
                date.append(result[i].__getattribute__("date"))
                link.append(result[i].__getattribute__("url"))
            status.update("Generating table...")
            
            # Sets up the table
            table = Table(title="\nSearch Results from Spotify", show_lines = True)
            table.add_column("ID", style="cyan", no_wrap = True)
            table.add_column("Name", style="dark_turquoise")
            table.add_column("Artist", style="gold1")
            table.add_column("Album", style="pale_violet_red1")
            table.add_column("Duration", style="magenta")
            table.add_column("Date", style="cornflower_blue")
            status.update(f"Printing table...")

        # Adds the data to the table
        for i in range(len(name)):
            table.add_row(str(i+1), name[i], artist[i], album[i], duration[i], date[i])
        print(table)

        # Asks user if their song is in the list
        while True:
            choice = input("Is the song you want to download in the list? (Y/N): ").strip().lower()
            if choice == "y":
                break
            elif choice == "n":
                print("[yellow]Please be more specific with your search.[/yellow]")
                clear()
                spotsearch()
                break
            else:
                print("[red]Invalid input.[/red]")
                continue
        
        # Asks user for the song ID to download
        while True:
            try:
                choice = int(input("Enter the ID of the song you want to download: "))
                if choice > len(name):
                    print("[red]Invalid ID.[/red]")
                    continue
                elif choice < 1:
                    print("[red]Invalid ID.[/red]")
                    continue
                return link[choice-1]
            except ValueError:
                print("[red]Invalid input.[/red]")
                continue

    except Exception:
        print("[red]Something went wrong. Please try again.[/red]")
        print("[red]Redirecting to previous screen...[/red]")
        return False


# Downloads the song
def download(query=None):
    if query is None:
        while True:
            query = input("Enter the link: ")
            if query == "":
                print("[red]Query cannot be blank.[/red]")
                continue
            elif not query.startswith("https://open.spotify.com"):
                print("[red]Invalid link.[/red]")
                continue
            break

    # Ask the user where to save the video
    while True:
        dir = input("Enter the path where you want to download the song(s) (default: current directory): ")
        if dir == "":
            dir = "."
            break
        elif os.path.isdir(dir):
            print(f"[green]Song will be downloaded to {dir}[/green]")
            break
        else:
            print("[red]Entered path is not a valid directory path[/red]")
            continue
    
    # Ask the user if they want to make a folder
    while True:
        choice = input("Do you want to make a folder for the song(s)? (Y/N): ").strip().lower()
        if choice == 'y':
            while True:
                folder = input("Enter the name of the folder: ")
                if folder == "":
                    folder = f"Spotify download {convert_time(datetime.now().strftime('%Y-%m-%d %H.%M.%S'))}"
                    parent = dir
                    dir = os.path.join(parent, folder)
                    os.mkdir(dir)
                    break
                else:
                    if not re.match('^(?!(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.[^.]*)?$)[^<>:"/\\|?*\x00-\x1F]*[^<>:"/\\|?*\x00-\x1F\ .]$', folder):
                        print("[red]Invalid folder name[/red]")
                        continue
                    parent = dir
                    dir = os.path.join(parent, folder)
                    os.mkdir(dir)
                    break
            break
        elif choice == 'n':
            break
        else:
            print("[red]Invalid input[/red]")
            continue
    
    # Download
    try:
        with console.status("Downloading song...", spinner="dots"):
            subprocess.run(f"spotdl download {query}", cwd = dir, text=True)
        return True
    except Exception:
        print("[red]Something went wrong. Please try again.[/red]")
        print("[red]Redirecting to previous screen...[/red]")
        return False
