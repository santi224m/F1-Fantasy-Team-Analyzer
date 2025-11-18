import json
from pathlib import Path

class Config:
  def __init__(self, config_file="config.json"):
    self.config_file = Path(config_file)
    self.data = self._load()

  def _load(self):
    """Load json config file"""
    if self.config_file.exists():
      with open(self.config_file, 'r') as f:
        return json.load(f)
    else:
      return {
        "DRIVER_STANDINGS_URL": None,
        "MY_TEAM_URL": None,
        "USER_COOKIE": None
      }
  
  def save(self):
    """Save json file"""
    with open(self.config_file, 'w') as f:
      json.dump(self.data, f, indent=2)
  
  def get(self, key, default=""):
    """Get a config value"""
    return self.data.get(key, default)

  def set(self, key, val):
    """Update a config value"""
    self.data[key] = val
    self.save()