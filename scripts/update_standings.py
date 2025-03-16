import asyncio
from os.path import isdir
from time import sleep

from pydoll.browser.chrome import Chrome
from pydoll.constants import By

async def run_scraper():
  # Start the browser with no additional webdriver configuration!
  f1_fantasy_url = "https://fantasy.formula1.com/en/create-team"
  async with Chrome() as browser:
    await browser.start()
    page = await browser.get_page()

    # Navigate through captcha-protected sites without worry
    await page.go_to(f1_fantasy_url)
    sleep(2)

if __name__ == "__main__":
  try:
    asyncio.run(run_scraper())
  except:
    print("Warning: Chrome must be installed for scraper to run.")
