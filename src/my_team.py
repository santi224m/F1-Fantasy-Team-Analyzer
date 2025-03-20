import os
import requests
from dotenv import load_dotenv

from fetch_standings import fetch_standings
from utils.Roster import Roster

def get_my_team():
  load_dotenv()
  url = "https://fantasy.formula1.com/services/user/gameplay/64a1a090-fee7-11ef-a647-75f1571865cc/getteam/1/1/2/1?buster=1742435023543"
  my_cookie = os.environ.get('MY_COOKIE')

  try:
    res = requests.get(url, headers={'Cookie': my_cookie})
    data = res.json()['Data']['Value']['userTeam'][0]['playerid']
  except:
    print("Error fetching team data. Try reseting auth cookie in '.env' file.")
    exit()
  drivers, constructors = fetch_standings()
  team = Roster()

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