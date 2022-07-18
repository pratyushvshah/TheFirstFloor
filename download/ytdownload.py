from pytube import YouTube, Playlist
from rich.table import Table
from rich import print
import os
import re
import urllib.request
from datetime import datetime
from dateutil import tz
import time
from miscellaneous.statfunc import clear, console


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


# Search for a video and returns false if not found or link if found
def ytsearch(query=None):
    clear()
    if query is None:
        while True:

            # Asks user for search query
            search_keyword = input("Enter the name of the video you want to search: ").strip()
            if search_keyword == "":
                print("[red]Invalid input.[/red]")
                continue
            break

        # Cleans up the search query
        search = ""
        for i in search_keyword:
            if i == " ":
                search += "+"
            else:
                if i.isalpha():
                    search += i
                else:
                    pass
        
    else:
        search_keyword = query

        # Cleans up the search query
        search = ""
        for i in search_keyword:
            if i == " ":
                search += "+"
            else:
                if i.isalpha():
                    search += i
                else:
                    pass

    # Searchs for the video
    with console.status(f"Generating search results for {search_keyword}...", spinner = "dots") as status:
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        if len(video_ids) == 0:
            print("[red]No results found. Redirecting to previous screen...[/red]")
            time.sleep(1.5)
            return False
        status.update(f"Found {len(video_ids)} results. Gathering information...")

        # Appends all required information to lists for printing in table
        titles = []
        duration = []
        author = []
        publishdate = []
        videolinks = []
        for video_id in video_ids:
            link = f"https://www.youtube.com/watch?v={video_id}"
            yt = YouTube(link)
            titles.append(yt.title)
            duration.append(seconds(yt.length))
            author.append(yt.author)
            publishdate.append(str(yt.publish_date.date()))
            videolinks.append(link)
        status.update(f"Generating table...")

        # Sets up the table
        table = Table(title="\nSearch Results from YouTube", show_lines = True)
        table.add_column("ID", style="dark_turquoise", no_wrap=True)
        table.add_column("Title", style="gold1")
        table.add_column("Duration", style="pale_violet_red1")
        table.add_column("Published", style="magenta")
        table.add_column("Author", style="cornflower_blue")
        status.update(f"Printing table...")

        # Adds the data to the table
        for i in range(len(titles)):
            table.add_row(str(i+1), titles[i], duration[i], publishdate[i], author[i])
        print(table)

    # Asks user if their song is in the list
    while True:
        choice = input("Is the song you want to download in the list? (Y/N): ").strip().lower()
        if choice == "y":
            break
        elif choice == "n":
            print("[yellow]Please be more specific with your search.[/yellow]")
            ytsearch()
            break
        else:
            print("[red]Invalid input.[/red]")
            continue
    
    # Asks user for the video ID to download
    while True:
        try:
            choice = int(input("Enter the ID of the video you want to download: "))
            if choice > len(titles):
                print("[red]Invalid input.[/red]")
                continue
            break
        except ValueError:
            print("[red]Invalid input.[/red]")
            continue
    return videolinks[choice-1]


# Download a single video
def one(link=None):

    # Ask for the link from user
    if link is None:
        while True:
            print("[yellow]NOTE: if you input playlist link, the first song will be downloaded[/yellow]")
            link = input("Enter the link of YouTube video you want to download: ")
            try:
                yt = YouTube(link)

                # If the link is not a youtube link, raise an error
                yt.title
                break
            except:
                print("[red]Invalid link[/red]")
                continue
    yt = YouTube(link)
            
    # Ask the user where to save the video
    while True:
        dir = input("Enter the path where you want to download the video (default: current directory): ")
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
        choice = input("Do you want to make a folder for the track? (Y/N): ").strip().lower()
        if choice == 'y':
            while True:
                folder = input("Enter the name of the folder: ")
                if folder == "":
                    folder = f"Track downloaded {convert_time(datetime.now().strftime('%Y-%m-%d %H.%M.%S'))}"
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

    # Ask for the choice of audio or video
    while True:
        choice = input("Do you want to download the audio only? (Y/N): ").strip().lower()
        if choice == 'y':
            ys = yt.streams.get_audio_only()
            break
        elif choice == 'n':
            ys = yt.streams.get_highest_resolution()
            break
        else:
            print("[red]Invalid input[/red]")
            continue
    
    # Variable to store the number of successful downloads
    successcount = 0
    failcount = 0

    # Starting download
    with console.status(f"Downloading {yt.title}", spinner = "dots"):
        try:
            ys.download(dir)
            print(f"\n[green]Downloaded {yt.title} successfully![/green]")
            successcount = 1
        except:
            print(f"\n[red]{yt.title} could not be downloaded.[/red]")
            failcount = 1
    print(f"Total 1 track(s). Successful download(s): {successcount}. Failed download(s): {failcount}.")


# Download a playlist
def many():

    # Ask for the link from user
    while True:
        try:
            songlist = Playlist(input("Enter the link of YouTube playlist you want to download: "))

            # If the link is not a youtube link, raise an error
            YouTube(songlist[0]).title
            break
        except Exception:
            print("[red]Invalid link[/red]")
            continue

    # Ask the user where to save the video
    while True:
        dir = input("Enter the path where you want to download the video (default: current directory): ")
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
        choice = input("Do you want to make a folder for the playlist? (Y/N): ").strip().lower()
        if choice == 'y':
            while True:
                folder = input("Enter the name of the folder: ")
                if folder == "":
                    folder = f"Playlist created {convert_time(datetime.now().strftime('%Y-%m-%d %H.%M.%S'))}"
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

    # Ask for the choice of audio or video
    while True:
        choice = input("Do you want to download the audio only? (Y/N): ").strip().lower()
        if choice == 'y':

            # Variable to store the number of successful downloads
            successcount = 0
            failcount = 0
            total = len(songlist)
            songcount = 0
            with console.status(f"Downloading Playlist", spinner = "dots") as status:
                for i in songlist:
                    songcount += 1
                    yt = YouTube(i)

                    # Gets the audio only stream
                    ys = yt.streams.get_audio_only()

                    # Downloads the stream
                    status.update(f"Downloading {songcount} of {total} tracks", spinner = "dots")
                    try:
                        ys.download(dir)
                        print(f"\n[green]Downloaded {yt.title} successfully![/green]")
                        successcount += 1
                    except Exception:
                        print(f"\n[red]{yt.title} could not be downloaded.[/red]")
                        failcount += 1
            print(f"[yellow]Total {len(songlist)} track(s).[/yellow] [green]Successful download(s): {successcount}.[/green] [red]Failed download(s): {failcount}.[/red]")
            break
        elif choice == 'n':

            # Variable to store the number of successful downloads
            successcount = 0
            failcount = 0
            total = len(songlist)
            songcount = 0
            with console.status(f"Downloading Playlist", spinner = "dots") as status:
                for i in songlist:
                    songcount += 1
                    yt = YouTube(i)

                    # Gets the audio only stream
                    ys = yt.streams.get_audio_only()

                    # Downloads the stream
                    status.update(f"Downloading {songcount} of {total} tracks", spinner = "dots")
                    try:
                        ys.download(dir)
                        print(f"\n[green]Downloaded {yt.title} successfully![/green]")
                        successcount += 1
                    except Exception:
                        print(f"\n[red]{yt.title} could not be downloaded.[/red]")
                        failcount += 1
            print(f"[yellow]Total {len(songlist)} track(s).[/yellow] [green]Successful download(s): {successcount}.[/green] [red]Failed download(s): {failcount}.[/red]")
            break
        else:
            print("[red]Invalid input[/red]")
            continue
