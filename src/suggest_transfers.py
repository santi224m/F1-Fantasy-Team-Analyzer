from rich.console import Console
from rich.table import Table

from find_best_team import find_top_team
from my_team import get_my_team
from fetch_standings import fetch_standings

def find_best_transfers(*, ALLOW_TRANSFERS=2, COST_CAP=100.0):
  top_teams = find_top_team(RETURN_COUNT=1000000, COST_CAP=COST_CAP)
  my_team = get_my_team()

  for team in top_teams:
    transfers_needed = team.diff(my_team)
    if len(transfers_needed) <= ALLOW_TRANSFERS:
      best_team = team
      break
  
  sell_ids = my_team.diff(best_team)
  buy_ids = best_team.diff(my_team)
  sell = []
  buy = []

  drivers, constructors = fetch_standings()

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

  console.print(transfer_table)


  points_table = Table(title="Projected Points")
  points_table.add_column("Old Team", justify="center", style="bright_red", no_wrap=True)
  points_table.add_column("New Team", justify="center", style="green1", no_wrap=True)
  points_table.add_row(str(my_team.projected), str(best_team.projected))
  console.print(points_table)
  print('\n'*2)

  best_team.print_table()

if __name__ == "__main__":
  find_best_transfers()