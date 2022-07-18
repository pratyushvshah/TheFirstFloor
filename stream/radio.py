from pyradios import RadioBrowser
from rich import print
from rich.table import Table
import subprocess # change os.system to subprocess
import os
from miscellaneous.statfunc import clear, mpvkeybindings

# Configures the class for search
rb = RadioBrowser()


# List of countries
def getcountry():

    # Gets a list of countries and sorts alphabetically
    countries = {i['name']:i['stationcount'] for i in rb.countries()}
    countries = dict(sorted(countries.items()))
    country = [i for i in countries.keys()]

    # Gets number of radio stations in country
    stations = [str(i) for i in countries.values()]

    # Sets up the table
    table = Table(title="Countries", show_lines = True)
    table.add_column("ID", style="dark_turquoise", no_wrap=True)
    table.add_column("Country", style="gold1")
    table.add_column("No. of stations", style="pale_violet_red1")

    # Adds data to the table
    for i in range(len(country)):
        table.add_row(str(i+1), country[i], stations[i])
    
    # Prints the table
    print(table)

    # Gets the ID of the country
    while True:
        choice = input("Please select the ID of the country whose radio stations you wish to listen to: ")
        
        # Error handling and returning the country
        try:
            choice = int(choice)
            if choice > len(country):
                print("[red]Invalid input.[/red]")
                print("w")
                continue
            elif choice < 1:
                print("[red]Invalid input.[/red]")
                print("a")
                continue
            else:
                return country[choice - 1]
        except ValueError:
            print("[red]Invalid input.[/red]")
            continue


# List of stations in a country
def getstation(country):
    clear()

    # Gets radio stations from a country whose links aren't broken
    stationinfo = rb.search(country=country, country_exact=True, hidebroken=True)
    stationname = [i['name'] for i in stationinfo]
    stationurl = [i['url'] for i in stationinfo]

    # Sets up the table
    table = Table(title=f"Stations in {country}", show_lines = True)
    table.add_column("ID", style="dark_turquoise", no_wrap=True)
    table.add_column("Station name", style="gold1")

    # Adds data to the table
    for i in range(len(stationname)):
        table.add_row(str(i+1), stationname[i])

    # Prints the table
    print(table)

    # Gets the ID of the station to play
    while True:
        choice = input("Please select the ID of the radio station you wish to listen to: ")
        
        # Error handling and gets the station link
        try:
            choice = int(choice)
            if choice > len(stationname):
                print("[red]Invalid input.[/red]")
                continue
            elif choice < 1:
                print("[red]Invalid input.[/red]")
                continue
            streamlink = stationurl[choice - 1]
            break
        except ValueError:
            print("[red]Invalid input.[/red]")
            continue
    
    # Plays station
    print(f"Playing {stationname[choice - 1]}...")
    print(mpvkeybindings)
    os.system(f"mpv --vid=no {streamlink}")
