import requests

from utils.Driver import Driver
from utils.Constructor import Constructor

def fetch_standings():
  url = "https://fantasy.formula1.com/feeds/drivers/2_en.json?buster=20250316135258"
  res = requests.get(url)
  fetch_res = res.json()['Data']['Value']
  drivers_json = [res for res in fetch_res if res['PositionName'] == "DRIVER"]
  constructors_json = [res for res in fetch_res if res['PositionName'] == "CONSTRUCTOR"]

  idx = 0
  drivers = {}
  constructors = {}

  for driver in drivers_json:
    d = Driver(driver['FUllName'], driver['Value'], float(driver['OverallPpints']), float(driver['ProjectedOverallPpints']))
    drivers[idx] = d
    idx += 1

  for constructor in constructors_json:
    c = Constructor(constructor['DisplayName'], constructor['Value'], float(constructor['OverallPpints']), float(constructor['ProjectedOverallPpints']))
    constructors[idx] = c
    idx += 1

  return (drivers, constructors)

if __name__ == "__main__":
  drivers, constructors = fetch_standings()
  bar = '='*20
  print(f"{bar} Drivers {bar}")
  for d in drivers.values():
    print(d.__dict__)

  print(f"{bar} Constructors {bar}")
  for c in constructors.values():
    print(c.__dict__)