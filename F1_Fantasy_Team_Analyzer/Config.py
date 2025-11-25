import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

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
        "TEAM_URL": None,
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

  def browser_update_config(self):
    """
    Update config values using browser
    """
    with sync_playwright() as p:
      # Set up browser and go to F1 login page
      browser = p.firefox.launch(headless=False)
      page = browser.new_page()
      page.goto("https://account.formula1.com/#/en/login")
      # btn = page.locator("iframe[title='SP Consent Message'] button[title='ACCEPT ALL']").is_visible()
      print(page.locator("iframe[title='SP Consent Message']").all())
      print(page.locator("iframe[title='SP Consent Message'] button").all())

      # Login
      # res = page.get_by_label("Email address")
      # page.get_by_label("Email address").fill("my email")
      # page.get_by_label("Password").fill("mypassword")
      # page.get_by_role("button", name="SIGN IN").click()

      browser.close()