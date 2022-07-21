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

SEARCHRESULTS = 0

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
def ytsearch(NUMSEARCHES, query=None):
    global SEARCHRESULTS
    SEARCHRESULTS = NUMSEARCHES
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
    
    # ID of results
    id = [str(i+1) for i in range(len(titles))]
    total = len(titles)

    # Gets number of search pages
    pages = int(total / SEARCHRESULTS) + 1

    # Navigation counter
    n = 0
    while n < pages:

        # Temporary lists for each page
        tmpid = []
        tmptitles = []
        tmpduration = []
        tmpauthor = []
        tmppublishdate = []
        if n == 0:
            try:
                tmpid = id[:SEARCHRESULTS]
                tmptitles = titles[:SEARCHRESULTS]
                tmpduration = duration[:SEARCHRESULTS]
                tmpauthor = author[:SEARCHRESULTS]
                tmppublishdate = publishdate[:SEARCHRESULTS]
            except IndexError:
                index = total % SEARCHRESULTS
                tmpid = id[-index:]
                tmptitles = titles[-index:]
                tmpduration = duration[-index:]
                tmpauthor = author[-index:]
                tmppublishdate = publishdate[-index:]
        else:
            try:
                tmpid = id[n*SEARCHRESULTS:(n+1)*SEARCHRESULTS]
                tmptitles = titles[n*SEARCHRESULTS:(n+1)*SEARCHRESULTS]
                tmpduration = duration[n*SEARCHRESULTS:(n+1)*SEARCHRESULTS]
                tmpauthor = author[n*SEARCHRESULTS:(n+1)*SEARCHRESULTS]
                tmppublishdate = publishdate[n*SEARCHRESULTS:(n+1)*SEARCHRESULTS]
            except IndexError:
                index = total % SEARCHRESULTS
                tmpid = id[-index:]
                tmptitles = titles[-index:]
                tmpduration = duration[-index:]
                tmpauthor = author[-index:]
                tmppublishdate = publishdate[-index:]

        # Sets up the table
        table = Table(title="\nSearch Results from YouTube", show_lines = True)
        table.add_column("ID", style="dark_turquoise", no_wrap=True)
        table.add_column("Title", style="gold1")
        table.add_column("Duration", style="pale_violet_red1")
        table.add_column("Published", style="magenta")
        table.add_column("Author", style="cornflower_blue")
        status.update(f"Printing table...")

        # Adds the data to the table
        for i in range(len(tmpid)):
            table.add_row(tmpid[i], tmptitles[i], tmpduration[i], tmppublishdate[i], tmpauthor[i])
        print(table)
        print(f"Showing results {tmpid[0]}-{tmpid[-1]} of {total}.")

        # Gets the ID of the song
        while True:
            choice = input("Press n to go to the next page, b to go back or enter the the ID of the video you want to download\n").lower().strip()
            
            # Error handling and returning the country
            try:
                if choice == "n":
                    if n == pages - 1:
                        clear()
                        n = 0
                        break
                    clear()
                    n += 1
                    break
                elif choice == "b":
                    if n == 0:
                        clear()
                        n = pages - 1
                        break
                    clear()
                    n -= 1
                    break
                else:
                    choice = int(choice)
                    if choice > total:
                        print("[red]Invalid input.[/red]")
                        continue
                    elif choice < 1:
                        print("[red]Invalid input.[/red]")
                        continue
                    else:
                        return videolinks[choice-1]
            except ValueError:
                print("[red]Invalid input.[/red]")
                continue


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
    time.sleep(1.5)


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
            time.sleep(1.5)
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
            time.sleep(1.5)
            break
        else:
            print("[red]Invalid input[/red]")
            continue
