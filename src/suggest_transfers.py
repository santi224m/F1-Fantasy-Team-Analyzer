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
      1: 25,
      2: 18,
      3: 15,
      4: 12,
      5: 10,
      6: 8,
      7: 6,
      8: 4,
      9: 2,
      10: 1,
      11: 0,
      12: 0,
      13: 0,
      14: 0,
      15: 0,
      16: 0,
      17: 0,
      18: 0,
      19: 0,
      20: 0,
      99: -26 # For drivers you don't want to be suggested
    }
    # Reset contructors points
    for id in constructors.keys():
      constructors[id].points = 0
    for id, driver in drivers.items():
      if '--csv' in argv:
        pos = predicted_standings.loc[driver.name].Pos
      else:
        pos = int(input(f"{driver.name} Pos: "))
      drivers[id].points = pos_map[pos]
      constructors[drivers[id].team_id].points += pos_map[pos]
      if id in my_team_d_ids or id in my_team_c_ids:
        my_team.points += pos_map[pos] * 2
    print()
  team_balance = my_team.cost + my_team.budget - .1
  top_teams = find_top_team(RETURN_COUNT=1000000, COST_CAP=team_balance, CUSTOM_STANDINGS=(drivers, constructors))

  for team in top_teams:
    transfers_needed = team.diff(my_team)
    if len(transfers_needed) <= ALLOW_TRANSFERS:
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
  best_team.print_table()

if __name__ == "__main__":
  find_best_transfers(ALLOW_TRANSFERS=2)