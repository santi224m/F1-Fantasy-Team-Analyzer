from sys import argv
from os import getcwd
from itertools import combinations, product

from bs4 import BeautifulSoup

# from rich.progress import Progress
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
)

from utils.Driver import Driver
from utils.Constructor import Constructor
from utils.Roster import Roster

def find_top_team(*, VERBOSE=False):
    base_path = '../data/' if 'scripts' in getcwd() else 'data/'
    drivers = {}
    idx = 0
    COST_CAP = 100.0

    # ---------------------------------------------------------------------------- #
    #                               PARSE DRIVER DATA                              #
    # ---------------------------------------------------------------------------- #
    with open(f"{base_path}drivers_html.txt", 'r') as html:
        soup = BeautifulSoup(html.read(), features="html.parser")

    # Iterate through drivers
    for player_li in soup.find_all('li'):
        # Get driver name
        img_tag = player_li.find('img')
        if (img_tag):
            driver_name = img_tag.get('alt')
        try:
            driver_points = int(player_li.find_all('div', {"class": "si-player__stats-nums"})[1].find('span').get_text().strip().split()[0])
        except:
            continue
        try:
            driver_price = float(player_li.find('span', {"class": "si-bgTxt"}).get_text().replace('$', '').replace('M', ''))
        except:
            continue
        drivers[idx] = Driver(driver_name, driver_price, driver_points)
        idx += 1

    # ---------------------------------------------------------------------------- #
    #                            PARSE CONSTRUCTOR DATA                            #
    # ---------------------------------------------------------------------------- #
    with open(f"{base_path}constructors_html.txt", 'r') as html:
        soup = BeautifulSoup(html.read(), features="html.parser")

    constructors = {}
    # Iterate through constructors
    for constructor_li in soup.find_all('li'):
        try:
            constructor_name = constructor_li.find('div', {"class": "si-player__name--constructor"}).find('span').get_text().strip()
        except: continue
        try:
            constructor_pts = int(constructor_li.find_all('div', {"class": "si-player__stats-nums"})[1].find('span').get_text().strip().split()[0])
        except: continue
        try:
            constructor_price = float(constructor_li.find('span', {'class': 'si-bgTxt'}).get_text().strip().replace('$', '').replace('M', ''))
        except: continue

        constructors[idx] = Constructor(constructor_name, constructor_price, constructor_pts)
        idx += 1

    # ---------------------------------------------------------------------------- #
    #                   CREATE COMBINATIONS OF ALL POSSIBLE TEAMS                  #
    # ---------------------------------------------------------------------------- #
    driver_ids = [id for id in drivers.keys()]
    constructor_ids = [id for id in constructors.keys()]

    driver_combinations = list(combinations(driver_ids, 5))
    constructor_combinations = list(combinations(constructor_ids, 2))
    teams = list(product(driver_combinations, constructor_combinations))
    if VERBOSE:
        print(f"Total possible combinations: {len(teams):,}")

    # ---------------------------------------------------------------------------- #
    #                             CALCULATE TEAM STATS                             #
    # ---------------------------------------------------------------------------- #
    valid_rosters = []
    with Progress(
        TextColumn("[bold grey100]Finding best team...", justify="right"),
        BarColumn(bar_width=None),
        "[progress.description]{task.completed:,}/{task.total:,} combinations",
        "•",
        TimeRemainingColumn(),
        ) as progress:
        task1 = progress.add_task("[grey100]Comparing Rosters...", total=len(teams))
        for team in teams:
            roster = Roster()

            # Add drivers to roster
            for driver_id in team[0]:
                roster.add_driver(drivers[driver_id])

            # Add constructors to roster
            for constructor_id in team[1]:
                roster.add_constructor(constructors[constructor_id])

            # Ensure total cost is under cost cap
            if roster.cost <= COST_CAP:
                valid_rosters.append(roster)

            progress.update(task1, advance=1)

    top_team = sorted(valid_rosters, key=lambda r: r.points, reverse=True)[0]
    return top_team

if __name__ == "__main__":
    verbose = True if '--verbose' in set(argv) else False
    top_team = find_top_team(VERBOSE=verbose)
    print()
    top_team.print_table()