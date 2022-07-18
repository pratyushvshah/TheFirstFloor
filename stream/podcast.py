import podsearch
from rich import print
from rich.table import Table
import time
from miscellaneous.statfunc import clear, console


def searcher():
    while True:

        # Asks user for search query
        search_keyword = input("Enter the name of the podcast you want to search: ").strip()
        if search_keyword == "":
            print("[red]Invalid input.[/red]")
            continue
        
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
        break
    while True:

        # Asks user for country of the podcast
        print("[yellow]NOTE: If you don't know the ISO Alpha-2 code of the country, check out[/yellow] [underline blue]https://www.iban.com/country-codes[/underline blue]")
        country = input("Enter the ISO Alpha-2 country code of the podcast you want to search (default US): ").strip().upper()
        if country == "":
            country = "US"
            break
        elif country not in ["AF", "AX", "AL", "DZ", "AS", "AD", "AO", "AI", "AQ", "AG", "AR", "AM", "AW", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT, BO, BQ, BA, BW, BV, BR, IO, BN, BG, BF, BI, CV, KH, CM, CA, KY, CF, TD, CL, CN, CX, CC, CO, KM, CD, CG", "CK", "CR", "CI", "HR", "CU", "CW", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "GQ", "ER", "EE", "SZ", "ET", "FK", "FO", "FJ", "FI", "FR", "GF", "PF", "TF", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT", "GG", "GN", "GW", "GY", "HT", "HM", "VA", "HN", "HK", "HU", "IS", "IN", "ID", "IR", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KP", "KR", "KW", "KG", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NC", "NZ", "NI", "NE", "NG", "NU", "NF", "MP", "NO", "OM", "PK", "PW", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "SH", "KN", "LC", "MF", "PM", "VC", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SX", "SK", "SI", "SB", "SO", "ZA", "GS", "SS", "ES", "LK", "SD", "SR", "SJ", "SE", "CH", "SY", "TW", "TJ", "TZ", "TH", "TL", "TG", "TK", "TO", "TT", "TN", "TR", "TM", "TC", "TV", "UG", "UA", "AE", "GB", "UM", "US", "UY", "UZ", "VU", "VE", "VN", "VG", "VI", "WF", "EH", "YE", "ZM", "ZW"]:
            print("[red]Invalid country code.[/red]")
            continue
    while True:

        # Asks user for the number of limit to be returned
        limit = input("Enter the number of limit you want to see (default 10): ").strip()
        if limit == "":
            limit = 10
            break
        elif limit.isdigit() == False:
            print("[red]Invalid input.[/red]")
            continue
        elif int(limit) > 50:
            print("[red]Too many search results.[/red]")
            continue
        elif int(limit) < 1:
            print("[red]Too few search results.[/red]")
            continue
        else:
            limit = int(limit)
            break
    with console.status(f"Searching for {search_keyword} in {country}", spinner="dots") as status:

        # Searches for the podcast
        results = podsearch.search(search, country = country, limit = limit)
        if len(results) == 0:
            print("[red]No results found. Redirecting to previous screen...[/red]")
            time.sleep(1.5)
            return False
        status.update(f"Found {len(results)} results. Gathering information...")

        # Appends all required information to lists for printing in table            
        name = []
        category = []
        author = []
        episodes = []
        link = []
        for i in results:
            name.append(i.name)
            category.append(i.category)
            author.append(i.author)
            episodes.append(i.episode_count)
            link.append(i.url)
        status.update(f"Generating table...")

        # Creates a table to display the results
        table = Table(title="\nSearch Results from Apple Podcasts", show_lines = True)
        table.add_column("ID", style="dark_turquoise", no_wrap = True)
        table.add_column("Title", style="gold1", no_wrap = True)
        table.add_column("Category", style="pale_violet_red1")
        table.add_column("Author", style="magenta")
        table.add_column("Epidodes", style="cornflower_blue")
        status.update(f"Printing table...")

        # Adds the data to the table
        for i in range(len(name)):
            table.add_row(str(i+1), name[i], category[i], author[i], str(episodes[i]))
        print(table)

    # Asks user if their song is in the list
    while True:
        choice = input("Is the podcast you want to listen to in the list? (Y/N): ").strip().lower()
        if choice == "y":
            break
        elif choice == "n":
            print("[yellow]Please be more specific with your search.[/yellow]")
            clear()
            searcher()
            break
        else:
            print("[red]Invalid input.[/red]")
            continue
    
    # Asks user for the video ID to download
    while True:
        try:
            choice = int(input("Enter the ID of the podcast you want to listen to: "))
            if choice > len(name):
                print("[red]Invalid input.[/red]")
                continue
            break
        except ValueError:
            print("[red]Invalid input.[/red]")
            continue
    return link[choice-1]
