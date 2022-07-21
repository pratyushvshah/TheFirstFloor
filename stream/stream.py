from telnetlib import SE
from pytube import YouTube
from rich.table import Table
from rich import print
import subprocess # change os.system to subprocess
import os
import re
import urllib.request
import time
from miscellaneous.statfunc import clear, console, mpvkeybindings

SEARCHRESULTS = 0

# Convert seconds to hours, minutes and seconds
def seconds(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)


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
        print(n)

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
            choice = input("Press n to go to the next page, b to go back or enter the the ID of the video you want to listen to\n").lower().strip()
            
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
