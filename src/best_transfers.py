from find_best_team import find_top_team
from my_team import get_my_team
from fetch_standings import fetch_standings

def find_best_transfers():
  ALLOW_TRANSFERS = 2
  top_teams = find_top_team(RETURN_COUNT=1000000)
  my_team = get_my_team()

  for team in top_teams:
    transfers_needed = team.diff(my_team)
    if len(transfers_needed) <= ALLOW_TRANSFERS:
      best_team = team
      break
  
  best_team.print_table()
  sell = my_team.diff(best_team)
  buy = best_team.diff(my_team)
  drivers, constructors = fetch_standings()
  for id in sell:
    if id in drivers:
      print('Sell: ', drivers[id].__dict__)
    elif id in constructors:
      print('Sell: ', constructors[id].__dict__)

  for id in buy:
    if id in drivers:
      print('Buy: ', drivers[id].__dict__)
    elif id in constructors:
      print('Buy: ', constructors[id].__dict__)

if __name__ == "__main__":
  find_best_transfers()