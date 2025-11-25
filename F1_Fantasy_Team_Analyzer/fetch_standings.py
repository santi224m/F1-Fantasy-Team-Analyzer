import requests
from rich.table import Table

from F1_Fantasy_Team_Analyzer.utils.Driver import Driver
from F1_Fantasy_Team_Analyzer.utils.Constructor import Constructor

def fetch_standings(console, config, *, method=None):
  # Get all drivers and constructors
  url = config.get('DRIVER_STANDINGS_URL')
  if url is None or url.strip() == "":
    raise Exception("Missing driver standings url. Please update config.")
  res = requests.get(url)
  fetch_res = res.json()['Data']['Value']
  drivers_json = [res for res in fetch_res if res['PositionName'] == "DRIVER" and res['IsActive'] == "1"]
  constructors_json = [res for res in fetch_res if res['PositionName'] == "CONSTRUCTOR"]

  # Extract drivers and constructors from JSON
  drivers = {}
  constructors = {}
  for driver in drivers_json:
    d = Driver(driver['PlayerId'], driver['TeamId'], driver['FUllName'], driver['Value'], float(driver['OverallPpints']))
    drivers[d.id] = d
  for constructor in constructors_json:
    c = Constructor(constructor['PlayerId'], constructor['DisplayName'], constructor['Value'], float(constructor['OverallPpints']))
    constructors[c.id] = c

  if method == 'last_race':
    # Get buster and next race id
    buster = url.split('buster=')[1]
    race_id = int(url.split('_en')[0].split('/')[-1])
    previous_race_id = race_id - 1
    console.clear()
    console.print("\n[yellow]Fetching driver's points for the last race...[/yellow]")
    for driver_id, driver in drivers.items():
      res = requests.get(f"https://fantasy.formula1.com/feeds/popup/playerstats_{driver_id}.json?buster={buster}")
      for gameday in res.json()['Value']['GamedayWiseStats']:
        if gameday['GamedayId'] == previous_race_id:
          last_race_points = gameday['StatsWise'][0]['Value']
          console.print(f"{driver.name}: {last_race_points}")
          driver.points = last_race_points
    console.clear()
    console.print("\n[yellow]Fetching constructors's points for the last race...[/yellow]")
    for constructor_id, constructor in constructors.items():
      res = requests.get(f"https://fantasy.formula1.com/feeds/popup/playerstats_{constructor_id}.json?buster=20251125031941")
      for gameday in res.json()['Value']['GamedayWiseStats']:
        if gameday['GamedayId'] == 22:
          last_race_points = gameday['StatsWise'][0]['Value']
          console.print(f"{constructor.name}: {last_race_points}")
          constructor.points = last_race_points
    console.clear()

  return (drivers, constructors)

def print_staindings(console, config, *, method=None):
  console.print("\n[yellow]Fetching standings...[/yellow]")
  drivers, constructors = fetch_standings(console, config, method=method)

  drivers_standings = sorted(drivers.values(), key=lambda d: d.points, reverse=True)
  constructors_standings = sorted(constructors.values(), key=lambda c: c.points, reverse=True)

  # ---------------------------------------------------------------------------- #
  #                                 DRIVERS TABLE                                #
  # ---------------------------------------------------------------------------- #
  drivers_table = Table(title="Driver Standings")
  drivers_table.add_column("", justify="center", style="white")
  drivers_table.add_column("Name", justify="center", style="grey100", no_wrap=True)
  drivers_table.add_column("Price", justify="right", style="dark_olive_green2")
  drivers_table.add_column("Points", justify="center", style="dark_slate_gray2")

  for idx, driver in enumerate(drivers_standings):
    drivers_table.add_row(
      str(idx + 1),
      driver.name,
      f"${driver.price}M",
      str(driver.points),
      )

  # ---------------------------------------------------------------------------- #
  #                              CONSTRUCTORS TABLE                              #
  # ---------------------------------------------------------------------------- #
  constructors_table = Table(title="Constructors Standings")
  constructors_table.add_column("", justify="center", style="white")
  constructors_table.add_column("Name", justify="center", style="grey100", no_wrap=True)
  constructors_table.add_column("Price", justify="right", style="dark_olive_green2")
  constructors_table.add_column("Points", justify="center", style="dark_slate_gray2")

  for idx, constructor in enumerate(constructors_standings):
    constructors_table.add_row(
      str(idx + 1),
      constructor.name,
      f"${constructor.price}M",
      str(constructor.points),
    )

  # Print tables
  console.clear()
  console.print(drivers_table)
  console.print(constructors_table)