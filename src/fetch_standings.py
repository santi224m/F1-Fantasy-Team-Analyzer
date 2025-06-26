import os
from sys import argv

import requests
from rich.console import Console
from rich.table import Table

from utils.Driver import Driver
from utils.Constructor import Constructor

from dotenv import load_dotenv

def fetch_standings():
  # For drivers who have double entries, record which ID not to use
  # Ex: Yuki has an ID for Racing Bulls an Red Bull, so exclude Racing Bulls Yuki
  EXCLUDE_DRIVERS_ID= set([
    "130",    # Yuki Tsunoda - Racing Bulls
    "114",    # Liam Lawson - Red Bull Racing
    "15",    # Jack Doohan - Alpine
  ])

  load_dotenv()
  url = os.environ.get('DRIVER_STANDINGS_URL')
  res = requests.get(url)
  fetch_res = res.json()['Data']['Value']
  drivers_json = [res for res in fetch_res if res['PositionName'] == "DRIVER"]
  constructors_json = [res for res in fetch_res if res['PositionName'] == "CONSTRUCTOR"]

  drivers = {}
  constructors = {}

  for driver in drivers_json:
    if driver['PlayerId'] in EXCLUDE_DRIVERS_ID: continue
    d = Driver(driver['PlayerId'], driver['TeamId'], driver['FUllName'], driver['Value'], float(driver['OverallPpints']), float(driver['ProjectedOverallPpints']))
    drivers[d.id] = d

  for constructor in constructors_json:
    c = Constructor(constructor['PlayerId'], constructor['DisplayName'], constructor['Value'], float(constructor['OverallPpints']), float(constructor['ProjectedOverallPpints']))
    constructors[c.id] = c

  return (drivers, constructors)

if __name__ == "__main__":
  drivers, constructors = fetch_standings()

  if '--projected' in argv:
    drivers_standings = sorted(drivers.values(), key=lambda d: d.projected, reverse=True)
    constructors_standings = sorted(constructors.values(), key=lambda c: c.projected, reverse=True)
  else:
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
  drivers_table.add_column("Projected Points", justify="center", style="dark_slate_gray2")

  for idx, driver in enumerate(drivers_standings):
    drivers_table.add_row(
      str(idx + 1),
      driver.name,
      f"${driver.price}M",
      str(driver.points),
      str(driver.projected)
      )

  # ---------------------------------------------------------------------------- #
  #                              CONSTRUCTORS TABLE                              #
  # ---------------------------------------------------------------------------- #
  constructors_table = Table(title="Constructors Standings")
  constructors_table.add_column("", justify="center", style="white")
  constructors_table.add_column("Name", justify="center", style="grey100", no_wrap=True)
  constructors_table.add_column("Price", justify="right", style="dark_olive_green2")
  constructors_table.add_column("Points", justify="center", style="dark_slate_gray2")
  constructors_table.add_column("Projected Points", justify="center", style="dark_slate_gray2")

  for idx, constructor in enumerate(constructors_standings):
    constructors_table.add_row(
      str(idx + 1),
      constructor.name,
      f"${constructor.price}M",
      str(constructor.points),
      str(constructor.projected)
    )

  # Print tables
  console = Console()
  console.print(drivers_table)
  console.print(constructors_table)