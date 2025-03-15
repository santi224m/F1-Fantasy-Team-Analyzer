from itertools import combinations, product

# Define our drivers and teams
drivers = [f"Driver_{i+1}" for i in range(20)]
teams = [f"Team_{i+1}" for i in range(10)]

# Generate all possible combinations
driver_combinations = list(combinations(drivers, 5))
team_combinations = list(combinations(teams, 2))

# Calculate the number of combinations
num_driver_combinations = len(driver_combinations)
num_team_combinations = len(team_combinations)
total_combinations = num_driver_combinations * num_team_combinations

print(f"Number of driver combinations: {num_driver_combinations}")
print(f"Number of team combinations: {num_team_combinations}")
print(f"Total number of combinations: {total_combinations}")

# If you need to iterate through all combinations:
for i, (selected_drivers, selected_teams) in enumerate(product(driver_combinations, team_combinations)):
    # This is where you would process each combination
    # For demonstration, let's just print a few
    if i < 3:  # Only print the first 3 combinations
        print(f"\nCombination {i+1}:")
        print(f"Selected drivers: {selected_drivers}")
        print(f"Selected teams: {selected_teams}")

# To access a specific combination (for example, the 100th one):
if total_combinations >= 100:
    combo_index = 99  # 0-indexed, so 99 refers to the 100th combination
    selected_drivers = driver_combinations[combo_index % num_driver_combinations]
    selected_teams = team_combinations[combo_index // num_driver_combinations]
    print(f"\n100th combination:")
    print(f"Selected drivers: {selected_drivers}")
    print(f"Selected teams: {selected_teams}")
