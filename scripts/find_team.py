from sys import argv
from os import getcwd
from itertools import combinations, product

from bs4 import BeautifulSoup

from utils.Driver import Driver
from utils.Constructor import Constructor

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
    results = []
    for team in teams:
        total_cost = 0
        total_points = 0

        roster = []

        # Calculate drivers cost
        for driver_id in team[0]:
            total_cost += drivers[driver_id].price
            total_points += drivers[driver_id].points
            roster.append(drivers[driver_id])

        # Calculate constructors cost
        for constructor_id in team[1]:
            total_cost += constructors[constructor_id].price
            total_points += constructors[constructor_id].points
            roster.append(constructors[constructor_id])

        # Ensure total cost is under cost cap
        if total_cost <= COST_CAP:
            results.append((roster, total_cost, total_points))

    # Print top team
    top_team = sorted(results, key=lambda r: r[2], reverse=True)[0]
    return top_team    

if __name__ == "__main__":
    verbose = True if '--verbose' in set(argv) else False
    top_team = find_top_team(VERBOSE=verbose)
    if verbose:
        print(top_team)