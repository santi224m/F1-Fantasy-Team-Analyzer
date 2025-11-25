from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from F1_Fantasy_Team_Analyzer import __name__ as pkg_name
from F1_Fantasy_Team_Analyzer import __version__

from F1_Fantasy_Team_Analyzer.Config import Config

from F1_Fantasy_Team_Analyzer.fetch_standings import print_staindings
from F1_Fantasy_Team_Analyzer.my_team import print_team
from F1_Fantasy_Team_Analyzer.find_best_team import print_top_team
from F1_Fantasy_Team_Analyzer.suggest_transfers import find_best_transfers

def display_main_menu(console):
  """
  Display main menu options.
  """
  menu_text = """
  [bold cyan]Main Menu[/bold cyan]

  [1] Show Current Team
  [2] Fetch Standings
  [3] Find Best Team
  [4] Suggest Transfers
  [8] Auto Update Config (WIP)
  [9] Update Config
  [0] Exit
  
  Please select an option:"""
  choices = ["1", "2", "3", "4", "8", "9", "0"]

  title = f"[bold green]{pkg_name}[/bold green]"
  subtitle = f"v{__version__}"
  border_style = "green"

  console.print(Panel(menu_text, title=title, subtitle=subtitle,
                      border_style=border_style))
  return choices

def display_config(console, config):
  """Display config file values"""
  table = Table(title="Config")
  table.add_column("idx", justify="center", style="white")
  table.add_column("Key", justify="left", style="magenta")
  table.add_column("Value", justify="right", style="green")
  
  idx_key_map = {}
  for idx, key in enumerate(config.data.keys()):
    idx_key_map[idx + 1] = key

  for idx, key in idx_key_map.items():
    table.add_row(str(idx), key, config.get(key))

  console.print(table)
  console.print("Enter 0 to exit\n")
  choices = [str(idx) for idx in idx_key_map.keys()]
  choices.append("0")
  return choices, idx_key_map

def main():
  """
  F1 Fantasy Team Analyzer

  This CLI tool is designed to help choose the best Formula 1 Fantasy
  team each race weekend.
  """
  # Load config
  config = Config()

  console = Console()
  
  while True:
    console.clear()
    choices = display_main_menu(console)

    choice = Prompt.ask("", choices=choices, show_choices=False)
    try:
      if choice == "0":
        console.print("[bold green]Thanks for using F1 Fantasy Team Analyzer![/bold green]")
        break
      elif choice == "1":
        console.clear()
        console.print("\n[yellow]Fetching current team...[/yellow]")
        print_team(console, config)
        Prompt.ask("Press ENTER to continue")
      elif choice == "2":
        print_staindings(console, config)
        Prompt.ask("Press ENTER to continue")
      elif choice == "3":
        console.clear()
        console.print("\n[yellow]Calculating best team...[/yellow]")
        print_top_team(console, config)
        Prompt.ask("Press ENTER to continue")
      elif choice == "4":
        console.clear()
        console.print("\n[yellow]Calculating best transfers...[/yellow]")
        find_best_transfers(config, ALLOW_TRANSFERS=3)
        Prompt.ask("Press ENTER to continue")
      elif choice == "8":
        config.browser_update_config()
        Prompt.ask("Press ENTER to continue")
      elif choice == "9":
        config_choices, idx_key_map = display_config(console, config)
        choice = Prompt.ask("Key to update", choices=config_choices, show_choices=True)
        if choice == "0":
          continue
        val = Prompt.ask("New value")
        key = idx_key_map[int(choice)]
        config.set(key, val)
    except Exception as e:
      console.clear()
      console.print(f"[bold red]Error: {e}[/bold red]")
      Prompt.ask("Press ENTER to continue")
  return 0