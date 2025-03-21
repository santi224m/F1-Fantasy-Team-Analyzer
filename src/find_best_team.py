from itertools import combinations, product
from contextlib import nullcontext

# from rich.progress import Progress
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
)

from fetch_standings import fetch_standings
from utils.Roster import Roster

def find_top_team(*, VERBOSE=False, RETURN_COUNT=0, COST_CAP=100.0, CUSTOM_STANDINGS=None):
    if CUSTOM_STANDINGS:
        drivers, constructors = CUSTOM_STANDINGS
    else:
        drivers, constructors = fetch_standings()

    # ---------------------------------------------------------------------------- #
    #                   CREATE COMBINATIONS OF ALL POSSIBLE TEAMS                  #
    # ---------------------------------------------------------------------------- #
    driver_ids = [id for id in drivers.keys()]
    constructor_ids = [id for id in constructors.keys()]

    driver_combinations = list(combinations(driver_ids, 5))
    constructor_combinations = list(combinations(constructor_ids, 2))
    teams = list(product(driver_combinations, constructor_combinations))

    # ---------------------------------------------------------------------------- #
    #                             CALCULATE TEAM STATS                             #
    # ---------------------------------------------------------------------------- #
    valid_rosters = []
    context_manager = Progress(
        TextColumn("[bold grey100]Finding best team...", justify="right"),
        BarColumn(bar_width=None),
        "[progress.description]{task.completed:,}/{task.total:,} combinations",
        "•",
        TimeRemainingColumn(),
        ) if VERBOSE else nullcontext()
    with context_manager as progress:
        if VERBOSE:
            task1 = progress.add_task("[grey100]Comparing Rosters...", total=len(teams))
        for team in teams:
            roster = Roster()

            # Add drivers to roster
            for driver_id in team[0]:
                roster.add_driver(drivers[driver_id])

            # Add constructors to roster
            for constructor_id in team[1]:
                roster.add_constructor(constructors[constructor_id])

            # Ensure total cost is under cost cap
            if roster.cost <= COST_CAP:
                valid_rosters.append(roster)

            if VERBOSE:
                progress.update(task1, advance=1)

    if RETURN_COUNT < len(valid_rosters):
        top_team = sorted(valid_rosters, key=lambda r: r.points, reverse=True)[RETURN_COUNT]
    else:
        top_team = sorted(valid_rosters, key=lambda r: r.points, reverse=True)
    return top_team

if __name__ == "__main__":
    top_team = find_top_team(VERBOSE=True)
    print()
    top_team.print_table()