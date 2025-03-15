from itertools import combinations, product

from bs4 import BeautifulSoup

if __name__ == "__main__":
    print("Calculating all combinations...")
    drivers = {}

    idx = 0
    with open("drivers_html.txt", 'r') as html:
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
            drive_price = float(player_li.find('span', {"class": "si-bgTxt"}).get_text().replace('$', '').replace('M', ''))
        except:
            continue
        drivers[idx] = (driver_name, driver_points, drive_price)
        idx += 1

    with open("constructors_html.txt", 'r') as html:
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

        constructors[idx] = (constructor_name, constructor_pts, constructor_price)
        idx += 1

    # Create combination of all possible teams
    driver_ids = [id for id in drivers.keys()]
    constructor_ids = [id for id in constructors.keys()]

    driver_combinations = list(combinations(driver_ids, 5))
    constructor_combinations = list(combinations(constructor_ids, 2))
    boost_combinations = list(combinations([0,1,2,3,4], 2))
    teams = list(product(driver_combinations, constructor_combinations, boost_combinations))

    # Iterate through all teams
    COST_CAP = 100.0
    results = []
    for team in teams:
        total_cost = 0
        drivers_cost = 0
        constructors_cost = 0
        total_points = 0

        boosted_drivers = team[2]
        roster = []

        # Calculate drivers cost
        for driver in team[0]:
            name, points, price = drivers[driver]
            drivers_cost += price
            roster.append(drivers[driver])
            total_points += points

        # Calculate constructors cost
        for constructor in team[1]:
            name, points, price = constructors[constructor]
            constructors_cost += price
            roster.append(constructors[constructor])
            total_points += points

        # Ensure total cost is under cost cap
        total_cost = drivers_cost + constructors_cost
        if total_cost <= COST_CAP:
            # Boosted drivers option 1
            boosted_points_1 = drivers[team[0][boosted_drivers[0]]][1]
            boosted_points_2 = drivers[team[0][boosted_drivers[1]]][1]
            results.append((roster, total_cost, total_points + (boosted_points_1 + (boosted_points_2 * 2))))
            results.append((roster, total_cost, total_points + ((boosted_points_1 * 2) + boosted_points_2)))

    print(sorted(results, key=lambda r: r[2], reverse=True)[0])

    # print("Done...")
    # search_points = int(input("Find team with how many points?: "))
    # found = set()
    # for team, cost, points in results:
    #     if points == search_points:
    #         names = ','.join(roster[0] for roster in sorted(team, key=lambda team_tup: team_tup[0]))
    #         if 'Piastri' in names and 'Yuki' not in names and 'Bearman' not in names and 'Hadjar' in names and 'Bortoleto' not in names and 'Alpine' not in names and 'Ocon' not in names and 'Gasly' not in names and 'Sainz' in names:
    #             found.add(names)
    # print(f"Found {len(found)} combinations with {search_points} points...")
    # print('='*100)
    # for t in found:
    #     print(t)