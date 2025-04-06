import os
import requests
from dotenv import load_dotenv

from fetch_standings import fetch_standings
from utils.Roster import Roster

def get_my_team():
  load_dotenv()
  url = os.environ.get('MY_TEAM_URL')
  my_cookie = os.environ.get('MY_COOKIE')

  try:
    res = requests.get(url, headers={'Cookie': my_cookie})
    data = res.json()['Data']['Value']['userTeam'][0]['playerid']
    team_balance = res.json()['Data']['Value']['userTeam'][0]['teambal']
  except:
    print("Error fetching team data. Try resetting auth cookie in '.env' file and make sure that MY_TEAM_URL is correct.")
    print("MY_TEAM_URL should have https://fantasy.formula1.com/services/user/gameplay/{SOME-UUID}/getteam/{SOME-NUMBER}/{SOME-NUMBER}/{SOME-NUMBER}/{SOME-NUMBER}?buster={SOME-NUMBER} format.")
    exit()
  drivers, constructors = fetch_standings()
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

if __name__ == "__main__":
  my_team = get_my_team()
  my_team.print_table()