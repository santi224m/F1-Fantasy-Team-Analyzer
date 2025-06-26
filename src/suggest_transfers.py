from sys import argv

import pandas as pd
from rich.console import Console
from rich.table import Table

from find_best_team import find_top_team
from my_team import get_my_team
from fetch_standings import fetch_standings

def find_best_transfers(*, ALLOW_TRANSFERS=2, COST_CAP=100.0):
  drivers, constructors = fetch_standings()
  my_team = get_my_team()
  if '--custom' in argv:
    if '--csv' in argv:
      predicted_standings = pd.read_csv('src/csv/predicted_standings.csv', index_col='Driver')
    my_team.points = 0
    my_team_d_ids = set([d.id for d in my_team.drivers])
    my_team_c_ids = set([c.id for c in my_team.constructors])
    pos_map = {
      1: 47,
      2: 35,
      3: 29,
      4: 22,
      5: 22,
      6: 17,
      7: 15,
      8: 15,
      9: 13,
      10: 12,
      11: 10,
      12: 7,
      13: 6,
      14: 5,
      15: 2,
      16: 2,
      17: 1,
      18: -2,
      19: -16,
      20: -20,
      99: -1000 # For drivers you don't want to be suggested
    }
    # Reset contructors points
    double_points = 0 # Add tops drivers points twice for 2x driver
    for id in constructors.keys():
      constructors[id].points = 0
    for id, driver in drivers.items():
      if '--csv' in argv:
        pos = predicted_standings.loc[driver.name].Pos
      else:
        pos = int(input(f"{driver.name} Pos: "))
      drivers[id].points = pos_map[pos]
      constructors[drivers[id].team_id].points += pos_map[pos]
      if id in my_team_d_ids:
        my_team.points += pos_map[pos]
        if pos_map[pos] > double_points:
          double_points = pos_map[pos]
    # Add contructor points back to my team
    for id, constructor in constructors.items():
      if id in my_team_c_ids:
        my_team.points += constructor.points
    # Add double points to 2x driver
    my_team.points += double_points
  team_balance = my_team.cost + my_team.budget - .1
  top_teams = find_top_team(RETURN_COUNT=1000000, COST_CAP=team_balance, CUSTOM_STANDINGS=(drivers, constructors))

  for team in top_teams:
    transfers_needed = team.diff(my_team)
    # Stop looking when we reach our current team, meaning we cannot improve
    if len(transfers_needed) == 0:
      best_team = team
      break

    if len(transfers_needed) <= ALLOW_TRANSFERS and team.points > my_team.points:
      best_team = team
      break

  sell_ids = my_team.diff(best_team)
  buy_ids = best_team.diff(my_team)
  sell = []
  buy = []

  for id in sell_ids:
    if id in drivers:
      sell.append(drivers[id])
    elif id in constructors:
      sell.append(constructors[id])

  for id in buy_ids:
    if id in drivers:
      buy.append(drivers[id])
    elif id in constructors:
      buy.append(constructors[id])

  console = Console()
  transfer_table = Table(title="Transfers")
  transfer_table.add_column("Sell", justify="center", style="bright_red", no_wrap=True)
  transfer_table.add_column("Buy", justify="center", style="green1", no_wrap=True)

  for idx in range(len(sell)):
    transfer_table.add_row(sell[idx].name, buy[idx].name)

  points_table = Table(title="Points")
  points_table.add_column("Old Team", justify="center", style="bright_red", no_wrap=True)
  points_table.add_column("New Team", justify="center", style="green1", no_wrap=True)
  points_table.add_row(str(my_team.points), str(best_team.points))

  console.print(transfer_table)
  console.print(points_table)
  print('\n'*2)
  best_team.print_table(team_balance=team_balance)

if __name__ == "__main__":
  find_best_transfers(ALLOW_TRANSFERS=2)
