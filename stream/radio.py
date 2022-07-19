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

    # ID of results
    id = [str(i+1) for i in range(len(countries))]
    total = len(countries)

    # Gets number of search pages
    pages = int(total / 10) + 1

    # Navigation counter
    n = 0
    while n < pages:

        # Temporary lists for each page
        tmpid = []
        tmpcountry = []
        tmpstations = []
        if n == 0:
            try:
                tmpid = id[:10]
                tmpcountry = country[:10]
                tmpstations = stations[:10]
            except IndexError:
                index = total % 10
                tmpid = id[-index:]
                tmpcountry = country[-index:]
                tmpstations = stations[-index:]
        else:
            try:
                tmpid = id[n*10:(n+1)*10]
                tmpcountry = country[n*10:(n+1)*10]
                tmpstations = stations[n*10:(n+1)*10]
            except IndexError:
                index = total % 10
                tmpid = id[-index:]
                tmpcountry = country[-index:]
                tmpstations = stations[-index:]

        # Sets up the table
        table = Table(title="Countries", show_lines = True)
        table.add_column("ID", style="dark_turquoise", no_wrap=True)
        table.add_column("Country", style="gold1")
        table.add_column("No. of stations", style="pale_violet_red1")

        # Adds data to the table
        for i in range(len(tmpid)):
            table.add_row(tmpid[i], tmpcountry[i], tmpstations[i])
        
        # Prints the table
        print(table)
        print(f"Showing results {tmpid[0]}-{tmpid[-1]} of {total}.")

        # Gets the ID of the country
        while True:
            choice = input("Press n to go to the next page, b to go back or enter the number of the country whose radio stations you wish to listen to.\n").lower().strip()
            
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

    # ID of results
    id = [str(i+1) for i in range(len(stationname))]
    total = len(stationname)

    # Gets number of search pages
    pages = int(total / 10) + 1

    # Navigation counter
    n = 0
    while n < pages:

        # Temporary lists for each page
        tmpid = []
        tmpstationname = []
        if n == 0:
            try:
                tmpid = id[:10]
                tmpstationname = stationname[:10]
            except IndexError:
                index = total % 10
                tmpid = id[-index:]
                tmpstationname = stationname[-index:]
        else:
            try:
                tmpid = id[n*10:(n+1)*10]
                tmpstationname = stationname[n*10:(n+1)*10]
            except IndexError:
                index = total % 10
                tmpid = id[-index:]
                tmpstationname = stationname[-index:]

        # Sets up the table
        table = Table(title=f"Stations in {country}", show_lines = True)
        table.add_column("ID", style="dark_turquoise", no_wrap=True)
        table.add_column("Station name", style="gold1")

        # Adds data to the table
        for i in range(len(tmpid)):
            table.add_row(tmpid[i], tmpstationname[i])

        # Prints the table
        print(table)
        print(f"Showing results {tmpid[0]}-{tmpid[-1]} of {total}.")

        # Gets the ID of the country
        while True:
            choice = input("Press n to go to the next page, b to go back or enter the ID of the radio station you wish to listen to.\n").lower().strip()
            
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
                        return stationname[choice - 1], stationurl[choice - 1]
            except ValueError:
                print("[red]Invalid input.[/red]")
                continue

def playradio(name, link):

    # Plays station
    print(f"Playing {name}...")
    print(mpvkeybindings)
    os.system(f"mpv --vid=no {link}")
