from os import getcwd
from itertools import combinations, product
from contextlib import nullcontext

import requests
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
    url = "https://fantasy.formula1.com/feeds/drivers/2_en.json?buster=20250316135258"
    res = requests.get(url)
    fetch_res = res.json()['Data']['Value']
    drivers_json = [res for res in fetch_res if res['PositionName'] == "DRIVER"]
    constructors_json = [res for res in fetch_res if res['PositionName'] == "CONSTRUCTOR"]

    drivers = {}
    constructors = {}
    idx = 0
    COST_CAP = 100.0

    for driver in drivers_json:
        d = Driver(driver['FUllName'], driver['Value'], float(driver['OverallPpints']))
        drivers[idx] = d
        idx += 1

    for constructor in constructors_json:
        c = Constructor(constructor['DisplayName'], constructor['Value'], float(constructor['OverallPpints']))
        constructors[idx] = c
        idx += 1

    # base_path = '../data/' if 'scripts' in getcwd() else 'data/'
    # drivers = {}
    # idx = 0
    # COST_CAP = 100.0

    # # ---------------------------------------------------------------------------- #
    # #                               PARSE DRIVER DATA                              #
    # # ---------------------------------------------------------------------------- #
    # with open(f"{base_path}drivers_html.txt", 'r') as html:
    #     soup = BeautifulSoup(html.read(), features="html.parser")

    # # Iterate through drivers
    # for player_li in soup.find_all('li'):
    #     # Get driver name
    #     img_tag = player_li.find('img')
    #     if (img_tag):
    #         driver_name = img_tag.get('alt')
    #     try:
    #         driver_points = int(player_li.find_all('div', {"class": "si-player__stats-nums"})[1].find('span').get_text().strip().split()[0])
    #     except:
    #         continue
    #     try:
    #         driver_price = float(player_li.find('span', {"class": "si-bgTxt"}).get_text().replace('$', '').replace('M', ''))
    #     except:
    #         continue
    #     drivers[idx] = Driver(driver_name, driver_price, driver_points)
    #     idx += 1

    # # ---------------------------------------------------------------------------- #
    # #                            PARSE CONSTRUCTOR DATA                            #
    # # ---------------------------------------------------------------------------- #
    # with open(f"{base_path}constructors_html.txt", 'r') as html:
    #     soup = BeautifulSoup(html.read(), features="html.parser")

    # constructors = {}
    # # Iterate through constructors
    # for constructor_li in soup.find_all('li'):
    #     try:
    #         constructor_name = constructor_li.find('div', {"class": "si-player__name--constructor"}).find('span').get_text().strip()
    #     except: continue
    #     try:
    #         constructor_pts = int(constructor_li.find_all('div', {"class": "si-player__stats-nums"})[1].find('span').get_text().strip().split()[0])
    #     except: continue
    #     try:
    #         constructor_price = float(constructor_li.find('span', {'class': 'si-bgTxt'}).get_text().strip().replace('$', '').replace('M', ''))
    #     except: continue

    #     constructors[idx] = Constructor(constructor_name, constructor_price, constructor_pts)
    #     idx += 1

    # ---------------------------------------------------------------------------- #
    #                   CREATE COMBINATIONS OF ALL POSSIBLE TEAMS                  #
    # ---------------------------------------------------------------------------- #
    driver_ids = [id for id in drivers.keys()]
    constructor_ids = [id for id in constructors.keys()]

    driver_combinations = list(combinations(driver_ids, 5))
    constructor_combinations = list(combinations(constructor_ids, 2))
    teams = list(product(driver_combinations, constructor_combinations))

    # ---------------------------------------------------------------------------- #
    #                             CALCULATE TEAM STATS                             #
    # ---------------------------------------------------------------------------- #
    valid_rosters = []
    context_manager = Progress(
        TextColumn("[bold grey100]Finding best team...", justify="right"),
        BarColumn(bar_width=None),
        "[progress.description]{task.completed:,}/{task.total:,} combinations",
        "•",
        TimeRemainingColumn(),
        ) if VERBOSE else nullcontext()
    with context_manager as progress:
        if VERBOSE:
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

            if VERBOSE:
                progress.update(task1, advance=1)

    top_team = sorted(valid_rosters, key=lambda r: r.points, reverse=True)[0]
    return top_team

if __name__ == "__main__":
    top_team = find_top_team(VERBOSE=True)
    print()
    top_team.print_table()