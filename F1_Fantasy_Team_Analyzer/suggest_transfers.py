
from rich.console import Console
from rich.table import Table

from F1_Fantasy_Team_Analyzer.find_best_team import find_top_team
from F1_Fantasy_Team_Analyzer.my_team import get_my_team
from F1_Fantasy_Team_Analyzer.fetch_standings import fetch_standings

def find_best_transfers(console, config, *, method=None):
  drivers, constructors = fetch_standings(console, config, method=method)
  my_team = get_my_team(console, config, method=method)
  team_balance = my_team.cost + my_team.budget - .1
  top_teams = find_top_team(config, RETURN_COUNT=1000000, COST_CAP=team_balance, CUSTOM_STANDINGS=(drivers, constructors))

  for team in top_teams:
    transfers_needed = team.diff(my_team)
    # Stop looking when we reach our current team, meaning we cannot improve
    if len(transfers_needed) == 0:
      best_team = team
      break

    if len(transfers_needed) <= my_team.subs_left and team.points > my_team.points:
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
  best_team.print_table(console, team_balance=team_balance)
