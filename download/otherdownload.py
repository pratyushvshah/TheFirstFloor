import yt_dlp
from rich import print
import os
import re
from datetime import datetime
from dateutil import tz
import os

currentdir = os.getcwd()
total = 0
successcount = 0
failcount = 0


# Special convert function to adhere with folder name requirements
def convert_time(time):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = datetime.strptime(time, '%Y-%m-%d %H.%M.%S')
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    return central.strftime('%Y-%m-%d %H.%M.%S')


# Custom progress hook to print progress to console
def my_hook(d):
    global total, successcount, failcount
    if d['status'] == 'finished':
        print(f'\n[green]{d["filename"]} downloaded successfully![/green]')
        successcount += 1
        total += 1
    elif d['status'] == 'downloading':
        pass
    elif d['status'] == 'error':
        failcount += 1
        total += 1
        print(f'\n[red]Something went wrong with downloading {d["filename"]}. Please try again[/red]')


# Download function
def download():
    global total, successcount, failcount

    # Ask user for url of the song to download
    while True:
        url = input('Enter the url of the song to download: ')
        if url == '':
            print('[red]Please enter a url![/red]')
        else:
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
                    folder = f"Misc. download {convert_time(datetime.now().strftime('%Y-%m-%d %H.%M.%S'))}"
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

    # Ask the user if they want to audio or video
    while True:
        choice = input("Do you want audio only? (Y/N): ").strip().lower()
        if choice == 'y':
            video = False
            break
        elif choice == 'n':
            video = True
            break
        else:
            print("[red]Invalid input[/red]")
            continue
    
    # Configure the downloader and download the song
    if video == False:
        ydl_opts = {
            'ignoreerrors': True,
            'format': 'ba',
            'progress_hooks': [my_hook],
            'quiet': True,
            'outtmpl': '%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            os.chdir(dir)
            ydl.download(url)
            os.chdir(currentdir)
            print(f"[yellow]Total {total} track(s).[/yellow] [green]Successful download(s): {successcount}.[/green] [red]Failed download(s): {failcount}.[/red]")
            total = 0
            successcount = 0
            failcount = 0
    else:
        ydl_opts = {
            'ignoreerrors': True,
            'format': 'bv+ba/b',
            'progress_hooks': [my_hook],
            'quiet': True,
            'outtmpl': '%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            os.chdir(dir)
            print("""
[yellow]NOTE: You will get two success messages for each song.
The first success message is for successfully downloading the best audio and video format.
The second success message is for successfully merging the audio and video files.[/yellow]
""")
            ydl.download(url)
            os.chdir(currentdir)
            print(f"[yellow]Total {total} track(s).[/yellow] [green]Successful download(s): {successcount}.[/green] [red]Failed download(s): {failcount}.[/red]")
            total = 0
            successcount = 0
            failcount = 0
