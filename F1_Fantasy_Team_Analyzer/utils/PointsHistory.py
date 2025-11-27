import requests
import pandas as pd

from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
)

from F1_Fantasy_Team_Analyzer.Config import Config

class PointsHistory:
  def __init__(self, drivers, constructors, *, console=None):
    self.drivers = drivers
    self.constructors = constructors
    self.console = console
    self.config = Config()

    # Extract buster from drivers url
    drivers_url = self.config.get('DRIVER_STANDINGS_URL')
    if drivers_url is None or drivers_url.strip() == "":
      raise Exception("Missing driver standings url. Please update config.")
    
    self.buster = drivers_url.split('buster=')[1]
    self.next_race_id = int(drivers_url.split('_en')[0].split('/')[-1])
    self.previous_race_id = self.next_race_id - 1
    self.drivers_history = pd.DataFrame()
    self.constructors_history = pd.DataFrame()
    self.load_history()

  def load_history(self):
    """
    Load history from JSON file if it exists
    or get from API ifit does not exist.
    """
    # TODO: Check if history JSON exists and load it if it does
    self.fetch_history()

  def fetch_history(self):
    """
    Fetch points history from F1 Fantasy API
    and store it in a pandas dataframe.
    Columns: ['DriverId', 'GamedayId', 'PlayerValue', 'RaceName', 'DriverName', 'Points']
    """
    driver_rows = []
    race_id_name_dict = {}

    if self.console:
      self.console.clear()

    context_manager = Progress(
      TextColumn("[bold grey100]Fetching points for all races this season...",justify="right"),
      BarColumn(bar_width=None),
      "[progress.description]{task.completed:,}/{task.total:,} stats",
      "•",
      TimeRemainingColumn(),
      )

    driver_ids = [key for key in self.drivers.keys()]
    constructor_ids = [key for key in self.constructors.keys()]
    all_ids = driver_ids + constructor_ids
    with context_manager as progress:
      task1 = progress.add_task("[grey100]Fetching drivers points...", total=30)
      for id in all_ids:
        res = requests.get(f"https://fantasy.formula1.com/feeds/popup/playerstats_{id}.json?buster={self.buster}")
        game_stats = res.json()['Value']['GamedayWiseStats']
        for game in game_stats:
          row = {}

          if len(race_id_name_dict.keys()) == 0:
            for race in res.json()['Value']['FixtureWiseStats']:
              race_id = race['GamedayId']
              for session in race['RaceDayWise']:
                if session['SessionType'] == 'Race':
                  race_id_name_dict[race_id] = session['MeetingName']

          row['Id'] = id
          row['GamedayId'] = game['GamedayId']
          row['PlayerValue'] = game['PlayerValue']
          row['RaceName'] = race_id_name_dict[game['GamedayId']]
          if id in driver_ids:
            row['Name'] = self.drivers[id].name
          else:
            row['Name'] = self.constructors[id].name
          if len(game['StatsWise']) > 0:
            row['Points'] = game['StatsWise'][0]['Value']
          else:
            row['Points'] = 0
          driver_rows.append(row)
        progress.update(task1, advance=1)
    df = pd.DataFrame(driver_rows)
    self.drivers_history = df

  def get_previous_race_points(self):
    """
    Return driver and constructor points for previous race.
    """
    # Get history stats for previous race
    prev = self.drivers_history[self.drivers_history['GamedayId'] == self.previous_race_id]
    # Update drivers points with previous race points
    for driver in self.drivers.values():
      driver.points = prev[prev['Id'] == driver.id].Points.iloc[0]

    # Update constructors points with previous race points
    for constructor in self.constructors.values():
      constructor.points = prev[prev['Id'] == constructor.id].Points.iloc[0]

    return (self.drivers, self.constructors)