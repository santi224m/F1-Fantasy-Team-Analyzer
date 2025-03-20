from rich.console import Console
from rich.table import Table

class Roster:
  def __init__(self):
    self.drivers = []
    self.constructors = []
    self.cost = 0.0
    self.points = 0
    self.MAX_DRIVERS = 5
    self.MAX_CONSTRUCTORS = 2

  def add_driver(self, driver):
    if len(self.drivers) == self.MAX_DRIVERS:
      raise ValueError("Roster full for drivers")
    self.drivers.append(driver)
    self.cost += driver.price
    self.points += driver.points

  def add_constructor(self, constructor):
    if len(self.constructors) == self.MAX_CONSTRUCTORS:
      raise ValueError("Roser full for constructors")
    self.constructors.append(constructor)
    self.cost += constructor.price
    self.points += constructor.points

  def print_table(self):
    # ---------------------------------------------------------------------------- #
    #                                 DRIVERS TABLE                                #
    # ---------------------------------------------------------------------------- #
    drivers_table = Table(title="F1 Fantasy Team Roster: Drivers")

    drivers_table.add_column("", justify="center", style="white")
    drivers_table.add_column("Driver", justify="center", style="grey100", no_wrap=True)
    drivers_table.add_column("Price", justify="center", style="dark_olive_green2")
    drivers_table.add_column("Points", justify="center", style="dark_slate_gray2")

    for idx, driver in enumerate(sorted(self.drivers, key=lambda driver: driver.points, reverse=True)):
      drivers_table.add_row(str(idx+1), driver.name, f"${driver.price:.1f}M", str(driver.points))

    # ---------------------------------------------------------------------------- #
    #                              CONSTRUCTORS TABLE                              #
    # ---------------------------------------------------------------------------- #
    constructors_table = Table(title="F1 Fantasy Team Roster: Constructors")

    constructors_table.add_column("", justify="center", style="white")
    constructors_table.add_column("Constructor", justify="center", style="grey100", no_wrap=True)
    constructors_table.add_column("Price", justify="center", style="dark_olive_green2")
    constructors_table.add_column("Points", justify="center", style="dark_slate_gray2")

    for idx, constructor in enumerate(sorted(self.constructors, key=lambda constructor: constructor.points, reverse=True)):
      constructors_table.add_row(str(idx+1), constructor.name, f"${constructor.price:.1f}M", str(constructor.points))

    # ---------------------------------------------------------------------------- #
    #                                 ROSTER STATS                                 #
    # ---------------------------------------------------------------------------- #
    stats_table = Table(title="Roster Stats")

    stats_table.add_column("Total Cost", justify="center", style="dark_olive_green2", no_wrap=True)
    stats_table.add_column("Total Points", justify="center", style="dark_slate_gray2")
    stats_table.add_row(f"${self.cost:.1f}M/$100.0M", str(self.points))

    # ---------------------------------------------------------------------------- #
    #                                 PRINT TABLES                                 #
    # ---------------------------------------------------------------------------- #
    console = Console()
    console.print(drivers_table)
    print()
    console.print(constructors_table)
    print()
    console.print(stats_table)

  def diff(self, other_roster):
    self_set = set([d.id for d in self.drivers] + [c.id for c in self.constructors])
    other_set = set([d.id for d in other_roster.drivers] + [c.id for c in other_roster.constructors])
    return self_set.difference(other_set)