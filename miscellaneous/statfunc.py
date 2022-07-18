import os
from datetime import datetime
from dateutil import tz
import logging
import traceback
import sys
from rich import print
from rich.console import Console

# Configure console for using rich module
console = Console()

mpvkeybindings = '''
p - Pause / playback mode
m - Mute / unmute audio
q - Quit
RIGHT / LEFT - Seek 5 seconds
UP / DOWN - Seek 60 seconds
[yellow]For a full list of options, visit: https://mpv.io/manual/master/#interactive-control [/yellow]
[yellow]If an error occurs, just hit enter to be redirected.[/yellow]
'''

# Clears terminal
def clear():
    os.system("cls||clear")


# Converts UTC to local time
def convert_time(time):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    return central.strftime('%Y-%m-%d %H:%M:%S')


# Prints banner
def banner():
    print("""                                                                                                 
 █|█|█|█|  █|█|█|  █|█|█|      █|█|█|  █|█|█|█|█|  █|█|█|█|  █|          █|█|      █|█|    █|█|█|    
 █|          █|    █|    █|  █|            █|      █|        █|        █|    █|  █|    █|  █|    █|  
 █|█|█|      █|    █|█|█|      █|█|        █|      █|█|█|    █|        █|    █|  █|    █|  █|█|█|    
 █|          █|    █|    █|        █|      █|      █|        █|        █|    █|  █|    █|  █|    █|  
 █|        █|█|█|  █|    █|  █|█|█|        █|      █|        █|█|█|█|    █|█|      █|█|    █|    █|

--------------------------------------WELCOME TO TheFirstFloor™------------------------------------
                                    We are the Poor Man's Spotify!
""", end="")


# Error logger
def errorlogging(exc_type, exc_value, exc_traceback):

    # Do not print exception when user cancels the program
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.basicConfig(filename = "ErrorLog.txt", level = logging.DEBUG)
    logging.error("An uncaught exception occurred:")
    logging.error("Type: %s", exc_type)
    logging.error("Value: %s", exc_value)

    if exc_traceback:
        format_exception = traceback.format_tb(exc_traceback)
        for line in format_exception:
            logging.error(repr(line.strip()))
            logging.error(repr(line.strip()))
