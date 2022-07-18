from ShazamAPI import Shazam
import os
from rich import print
from miscellaneous.statfunc import console
import sounddevice as sd
from scipy.io.wavfile import write


def recognize():

    # Asks user if they want to use a file to identify a song
    choice = input("Do you want to use a file to recognize the song? (Y/N) ").strip().lower()
    while True:
        if choice == "y":
            while True:

                # Gets path to file
                dir = input("Enter the path to the file you want to recognize: ")

                # Validates path
                if os.path.isfile(dir):
                    print(f"Analyzing the file at {dir}")
                    break
                else:
                    print("[red]Entered path is not a valid file path[/red]")
                    continue
        elif choice == "n":
            freq = 44100
            while True:

                # Gets duration for recording
                print("[yellow]It is recommeded to record atleast 15 seconds of audio to recognize the song.[/yellow]")
                duration = input("How long do you want to record for? (in seconds) ")
                try:
                    duration = int(duration)
                except ValueError:
                    print(f"[red]Invalid duration given, please enter a number")
                    continue
                if not 0 < duration <= 60:
                    print(f"[red]Record time is not in range [0-60]: {duration}")
                    continue
                break
            
            # Records audio
            with console.status("Recording...", spinner="dots"):
                recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
                sd.wait()
            
            # Stores audio in a temporary directory and deletes it after analysing
            os.mkdir("tmp")
            write("tmp/temp.wav", freq, recording)
            dir = "tmp/temp.wav"
            break       
        else:
            print("[red]Invalid input.[/red]")
            continue
    try:
        with console.status(f"Analyzing the file at {dir}") as status:
            
            # Opens file to analyze
            filetorecognize = open(dir, 'rb').read()
            shazam = Shazam(filetorecognize)
            status.update(f"Recognizing the song...")
            
            # Prints result or raises error if no result is found
            recognize_generator = shazam.recognizeSong()
            status.update(f"Printing the result...")
            
            # Gets the information about the song
            title = next(recognize_generator)[1]['track']['title']
            subtitle = next(recognize_generator)[1]['track']['subtitle']
            print(f"\n[yellow]The song is {title} - {subtitle}[/yellow]")
            
            # Deletes the temporary directory if it exists
            if dir == "tmp/temp.wav":
                os.remove("tmp/temp.wav")
                os.rmdir("tmp")
        
        # Asks user if they wish to download the song
        while True:
            choice = input("Do you want to download the song? (Y/N) ").strip().lower()
            if choice == "y":
                return True, "download", title, subtitle
            elif choice == "n":
                return True, "no", "no", "no"
            else:
                print("[red]Invalid choice[/red]")
                continue
    
    # Error message if no result is found
    except Exception:
        print(f"[red]Song not recognized.[/red]")
        if dir == "tmp/temp.wav":
                os.remove("tmp/temp.wav")
                os.rmdir("tmp")
        return False, "no", "no", "no"
