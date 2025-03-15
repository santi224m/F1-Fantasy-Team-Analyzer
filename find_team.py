from bs4 import BeautifulSoup

if __name__ == "__main__":
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
    idx = 0
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
    
    print(constructors)
