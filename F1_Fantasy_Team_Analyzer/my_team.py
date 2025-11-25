import requests

from F1_Fantasy_Team_Analyzer.fetch_standings import fetch_standings
from F1_Fantasy_Team_Analyzer.utils.Roster import Roster

def get_my_team(config):
  url = config.get('TEAM_URL')
  if url is None or url.strip() == "":
    raise Exception("Missing team url")
  user_cookie = config.get('USER_COOKIE')
  if user_cookie is None or user_cookie.strip() == "":
    raise Exception("Missing user cookie")

  try:
    res = requests.get(url, headers={'Cookie': user_cookie})
    data = res.json()['Data']['Value']['userTeam'][0]['playerid']
    team_balance = res.json()['Data']['Value']['userTeam'][0]['teambal']
  except:
    print("Error fetching team data. Try updating cookie.")
    exit()
  drivers, constructors = fetch_standings(config)
  team = Roster()
  team.set_budget(team_balance)

  for member in data:
    id = member['id']
    if id in drivers:
      driver = drivers[id]
      team.add_driver(driver)
    elif id in constructors:
      constructor = constructors[id]
      team.add_constructor(constructor)
  
  return team

def print_team(console, config):
  my_team = get_my_team(config)
  my_team_balance = my_team.cost + my_team.budget - .1
  console.clear()
  my_team.print_table(console, team_balance=my_team_balance)