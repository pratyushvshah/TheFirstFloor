import sys
import time
import sqlalchemy as sql
from rich import print
import webbrowser
import filekeys
import miscellaneous.settings as settings
import miscellaneous.login as login
from miscellaneous.statfunc import clear, banner, errorlogging, console
import download.ytdownload as ytdownload
import download.spotifydownload as spotifydownload
import download.otherdownload as otherdownload
import stream.stream as songstream
import stream.podcast as podcast
import stream.radio as radio
import recognize.shazam as shazam

# Initial cleating of the terminal
clear()

# Connects to database
with console.status("Connecting to the database...", spinner = "dots"):
    eng = sql.create_engine(f"{filekeys.postgresqllink}", isolation_level="AUTOCOMMIT")
    db = eng.connect()
    time.sleep(1.5)

NUMSEARCHES = 0

def main():
    username = loginblock()
    menu(username)


# Returns username
def loginblock():
    clear()
    banner()
    while True:
        choice = input('''
Hit 1 to Login
Hit 2 to Register an account with TheFirstFloor™ 
''').strip()
        if choice == '1':
            clear()
            banner()
            username = login.login()
            updatesettings(username)
            return username
        elif choice == '2':
            clear()
            banner()
            while True:
                result, msg = login.create_user()
                if result == False:
                    clear()
                    banner()
                    print()
                    print(f'[red]Invalid input: {msg}[/red]')
                    continue
                else:
                    clear()
                    banner()
                    print()
                    print(f'[green]{msg}[/green]')
                    username = login.login()
                    updatesettings(username)
                    return username
        else:
            loginblock()


# Main Menu
def menu(username):
    clear()
    banner()
    name = db.execute('SELECT fullname FROM users WHERE username = %s', username).fetchall()[0]._asdict()
    name = name['fullname']
    print(f'\nWelcome to TheFirstFloor™, {name}!')
    print('''
----------------------------------------MAIN MENU--------------------------------------------------
Hit 1 to stream music
Hit 2 to download songs
Hit 3 to search for podcasts
Hit 4 to listen to radio
Hit 5 to identify songs
Hit 6 to change settings
Hit 9 to quit
''', end="")
    while True:
        choice = input("")
        if choice not in ['1', '2', '3', '4', '5','6', '9']:
            menu(username)
        choice = int(choice)
        if choice == 1:
            stream(username)
        elif choice == 2:
            download(username)
        elif choice == 3:
            podcastsearch(username)
        elif choice == 4:
            radiostream(username)
        elif choice == 5:
            identify(username)
        elif choice == 6:
            changesettings(username)
        elif choice == 9:
            clear()
            banner()
            sys.exit('''
                                 Thank you for using TheFirstFloor™!
''')


# Stream music
def stream(username):
    clear()
    banner()
    print('''
----------------------------------------------STREAM-----------------------------------------------
Hit 1 if you are unsure of the link of the song you want to listen to.
Hit 2 if you have the link of the song you want to listen to.
Hit 9 if you want to return to the previous screen.
''')
    choice = input("")
    if choice == '1':
        result = songstream.ytsearch(NUMSEARCHES)
        if result == False:
            stream(username)
        else:
            songstream.onlinestream(result)
    elif choice == '2':
        songstream.onlinestream()
    elif choice == '9':
        menu(username)
    else:
        stream(username)


# Download music
def download(username):
    clear()
    banner()
    print('''
---------------------------------------------DOWNLOAD----------------------------------------------
Hit 1 to download from YouTube
Hit 2 to download from Spotify
Hit 3 to download from other sources (e.g. Soundcloud)
Hit 9 to return to the menu
''')
    choice = input("")
    if choice == '1':
        youtubedownloader(username)
    elif choice == '2':
        spotifydownloader(username)
    elif choice == '3':
        miscdownloader(username)
    elif choice == '9':
        clear()
        banner()
        menu(username)
    else:
        download(username)


# Download videos from YouTube
def youtubedownloader(username):
    clear()
    banner()
    choice = input('''
----------------------------------------------YOUTUBE----------------------------------------------
Hit 1 if you are unsure of the video link
Hit 2 to download 1 track
Hit 3 to download a playlist
Hit 9 to return to the previous screen
''')
    if choice == '1':
        result = ytdownload.ytsearch(NUMSEARCHES)
        if result == False:
            youtubedownloader(username)
        else:
            clear()
            ytdownload.one(result)
            youtubedownloader(username)
    elif choice == '2':
        clear()
        ytdownload.one()
        youtubedownloader(username)
    elif choice == '3':
        clear()
        ytdownload.many()
        youtubedownloader(username)
    elif choice == '9':
        download(username)
    else:
        youtubedownloader(username)


# Download songs from Spotify
def spotifydownloader(username):
    clear()
    banner()
    choice = input('''
----------------------------------------------SPOTIFY----------------------------------------------
For the query you have the following options:
Hit 1 if you are unsure of the spotify link
Hit 2 if you want to download 1 song
Hit 3 if you want to download a playlist
Hit 4 if you want to download all the songs in an album
Hit 5 if you want to download all the songs by an artist
Hit 9 to return to the previous screen
''')
    if choice == '1':
        clear()
        result = spotifydownload.spotsearch()
        if result == False:
            spotifydownloader(username)
        else:
            clear()
            spotifydownload.download(result)
            spotifydownloader(username)
    elif choice in ['2', '3', '4', '5']:
        clear()
        spotifydownload.download()
    elif choice == '9':
        download(username)
    else:
        spotifydownloader(username)


# Download songs from other sources
def miscdownloader(username):
    clear()
    banner()
    print('''
-----------------------------------------------MISC------------------------------------------------
''')
    otherdownload.download()
    while True:
        choice = input("Do you want to download another song? (Y/N) ").strip().lower()
        if choice == 'y':
            miscdownloader(username)
        elif choice == 'n':
            download(username)
        else:
            print("[red]Invalid input[/red]")
            continue


# Searches for podcasts
def podcastsearch(username):
    clear()
    banner()
    print('''
----------------------------------------------PODCAST----------------------------------------------
''')
    result = podcast.searcher()
    if result == False:
        clear()
        banner()
        menu(username)
    else:
        webbrowser.open(result, new=0, autoraise=True)
        while True:
            choice = input("Would you like to search for another podcast? (Y/N) ").strip().lower()
            if choice == 'y':
                clear()
                banner()
                podcastsearch(username)
            elif choice == 'n':
                clear()
                banner()
                menu(username)
            else:
                print('[red]Invalid input[/red]')
                continue


# Listen to radio
def radiostream(username):
    clear()
    banner()
    choice = input('''
-------------------------------------------------RADIO----------------------------------------------
Hit any key to continue
Hit 9 to return to menu
''')
    if choice == '9':
        menu(username)
    else:
        country = radio.getcountry(NUMSEARCHES)
        name, link = radio.getstation(country, NUMSEARCHES)
        radio.playradio(name, link)
        radiostream(username)


# Identify songs
def identify(username):
    clear()
    banner()
    print('''
------------------------------------------------SHAZAM---------------------------------------------
''')
    result, option, query1, query2 = shazam.recognize()
    if result == False or (result == True and option == "no"):
        
        # Asks user if they want to try again if they dont wish to download
        while True:
            choice = input("Would you like to try again? (Y/N) ").strip().lower()
            if choice == 'y':
                clear()
                banner()
                identify(username)
            elif choice == 'n':
                clear()
                banner()
                menu(username)
            else:
                print('[red]Invalid input[/red]')
                continue
    else:
        clear()
        banner()
        query = query1 + " " + query2
        
        # If the user wants to download the song, program does a youtube search for the result
        result = ytdownload.ytsearch(NUMSEARCHES, query)
        
        # If no song is found, returns to identifying menu
        if result == False:
            clear()
            banner()
            identify(username)
        
        # Download the song
        else:
            clear()
            ytdownload.one(result)
            clear()
            banner()
            
            # Asks the user if they want to try again
            while True:
                choice = input("Would you like to try again? (Y/N) ").strip().lower()
                if choice == 'y':
                    clear()
                    banner()
                    identify(username)
                elif choice == 'n':
                    clear()
                    banner()
                    menu(username)
                else:
                    print('[red]Invalid input[/red]')
                    continue


def changesettings(username):
    global NUMSEARCHES
    clear()
    banner()
    choice = input('''
----------------------------------------------SETTINGS---------------------------------------------
Hit 1 to change your username
Hit 2 to change your password
Hit 3 to change the number of search results per page
Hit 9 to return to the menu
''')
    while True:
        if choice == '1':
            clear()
            banner()
            result, newusername = settings.changeusername(username)
            if result == False:
                changesettings(username)
            else:
                username = newusername
            changesettings(username)
        elif choice == '2':
            clear()
            banner()
            settings.changepassword(username)
            changesettings(username)
        elif choice == '3':
            clear()
            banner()
            results, num = settings.changesearchresults(username, NUMSEARCHES)
            if results == False:
                changesettings(num)
            NUMSEARCHES = num
            updatesettings(username)
            changesettings(username)
        elif choice == '9':
            menu(username)
        else:
            changesettings(username)


# Updates global variables for user settings
def updatesettings(username):
    global NUMSEARCHES
    NUMSEARCHES = db.execute('SELECT numsearches FROM musicsettings WHERE username = %s', username).fetchall()[0]._asdict()['numsearches']

if __name__ == '__main__':

    # Override the default exception handling
    #sys.excepthook = errorlogging
    main()
