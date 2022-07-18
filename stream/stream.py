from pytube import YouTube
from rich.table import Table
from rich import print
import subprocess # change os.system to subprocess
import os
import re
import urllib.request
import time
from miscellaneous.statfunc import clear, console, mpvkeybindings


# Convert seconds to hours, minutes and seconds
def seconds(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)


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
        choice = input("Is the song you want to listen to in the list? (Y/N): ").strip().lower()
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
            choice = int(input("Enter the ID of the video you want to listen to: "))
            if choice > len(titles):
                print("[red]Invalid input.[/red]")
                continue
            break
        except ValueError:
            print("[red]Invalid input.[/red]")
            continue
    return videolinks[choice-1]


# Streams song
def onlinestream(link=None):
    clear()

    # Gets link of song to listen to
    if link is None:
        link = input("Enter the link of the song you want to listen to: ").strip()
    
    # Prompts user if they want to listen to audio only or show video
    while True:
            choice = input("Do you want to stream only audio? (Y/N) ").strip().lower()
            if choice == 'y':
                print(mpvkeybindings)
                os.system(f"mpv --vid=no {link}")
                break
            elif choice == 'n':
                print(mpvkeybindings)
                os.system(f"mpv {link}")
                break
            else:
                print("[red]Invalid input.[/red]")
                continue
