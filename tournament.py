import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# validations
def validate_id(id):
    try:
        val = int(id)
    except (ValueError, TypeError):
        logging.warning(f"Invalid ID input type: {id}")
        raise ValueError(f"{id} is not a valid integer")
    if val < 1:
        logging.warning(f"Non-positive ID input: {id}")
        raise ValueError(f"{id} is not a positive integer")

def validate_name(name): 
    if not name or name.strip() == "":
        logging.warning(f"Empty team name attempted.")
        raise ValueError(f"name cannot be empty!")

def check_if_id_and_name_exist(teams, id, name):
    for team in teams:
        if team["id"] == int(id) :
            logging.warning(f"Duplicate team ID attempt: {id}")
            raise ValueError(f"{id} already exist!")
        elif team["name"].lower() == name.strip().lower(): 
            logging.warning(f"Duplicate team Name attempt: {name}")           
            raise ValueError(f"{name} already exist!")

# task 1
def add_team(teams_list, id, name):
    validate_id(id)
    validate_name(name)
    check_if_id_and_name_exist(teams_list, id, name)
    team = {
    "id": int(id),
    "name": name.strip(), 
    "played": 0,
    "wins": 0, 
    "draws": 0, 
    "losses": 0,
    "goals_for": 0, 
    "goals_against": 0, 
    "points": 0
    }
    teams_list.append(team)
    logging.info(f"Team added successfully: ID {id}, Name {name.strip()}")

# task 2           
def show_teams(teams):
    if teams:
        for team in teams:
            print(f"ID: {team['id']}, Name: {team['name']}, Played: {team['played']}, Points: {team['points']}")
    else:
        print("There are no teams to show.")

# validations
def validate_goals(goals):
    try:
        val = int(goals)
    except (ValueError, TypeError):
        logging.warning(f"Invalid goals input type: {goals}")
        raise ValueError(f"{goals} is not a valid integer")
    if val < 0:
        logging.warning(f"Negative goals input: {goals}")
        raise ValueError(f"{goals} is not a positive integer")

def check_if_id_exist(teams, id):
    for team in teams:
        if team["id"] == int(id):
            return
    logging.warning(f"Team ID does not exist: {id}")
    raise ValueError(f"{id} is not exist!")

def check_if_played(matches, home_team_id, away_team_id):
    for match in matches:
        if ((home_team_id == match["home_team_id"] 
        or home_team_id == match["away_team_id"]) 
        and (away_team_id == match["home_team_id"] 
        or away_team_id == match["away_team_id"])):
            logging.warning(f"Duplicate match attempt between team {home_team_id} and team {away_team_id}")
            raise ValueError(f"{home_team_id} and {away_team_id} already played!")

# task 3
def add_matches(teams, matches, home_team_id, away_team_id, home_goals, away_goals):
    if home_team_id == away_team_id:
        logging.warning(f"Attempted match between a team and itself")
        raise ValueError("A team cannot play against itself!")
    check_if_id_exist(teams, home_team_id)
    check_if_id_exist(teams, away_team_id)
    validate_goals(home_goals)
    validate_goals(away_goals)
    check_if_played(matches, home_team_id, away_team_id)
    match = {
    "home_team_id": home_team_id,
    "away_team_id": away_team_id,
    "home_goals": int(home_goals),
    "away_goals": int(away_goals)
    }
    matches.append(match)
    update_team(teams, home_team_id, away_team_id, match)
    logging.info(f"Match added: Home ID {home_team_id} vs Away ID {away_team_id} ({home_goals}-{away_goals})")
       
def update_team(teams, home_team_id, away_team_id, match):
    home_points, away_points= calculate_points(match)
    for team in teams:
        if team["id"] == home_team_id:
            team["played"] += 1
            team["points"] += home_points
            if home_points == 3:
                team["wins"] += 1
            elif home_points == 1:
                team["draws"] += 1 
            else:
                team["losses"] += 1
            team["goals_for"] += match["home_goals"]
            team["goals_against"] += match["away_goals"]
        elif team["id"] == away_team_id:
            team["played"] += 1
            team["points"] += away_points
            if away_points == 3:
                team["wins"] += 1
            elif away_points == 1:
                team["draws"] += 1 
            else:
                team["losses"] += 1
            team["goals_for"] += match["away_goals"]
            team["goals_against"] += match["home_goals"]    

# task 4
def calculate_points(match):
    home_points = 0
    away_points = 0
    home_goals = match["home_goals"]
    away_goals = match["away_goals"]

    if home_goals == away_goals:
        home_points = 1
        away_points = 1
    elif home_goals > away_goals:
        home_points = 3
    else:
        away_points = 3
    return (home_points, away_points)

# task 5
def sort_teams(teams):
    if not teams:
        logging.warning("Attempted to sort teams, but the teams list is empty.")
        raise ValueError("There are no teams to show.")
    s1 = sorted(teams, key=lambda t: t["name"].lower())
    s2 = sorted(s1, key=lambda t: t["goals_for"], reverse=True)
    s3 = sorted(s2, key=lambda t: t["goals_for"] - t["goals_against"], reverse=True)
    sorted_teams = sorted(s3, key=lambda t: t["points"], reverse=True)    
    return sorted_teams

def show_sorted_teams(sorted_teams):
    for team in sorted_teams:
        deference_goals = team["goals_for"] - team["goals_against"]
        print(f"Name: {team['name']}, played: {team['played']}, wins: {team['wins']}, draws: {team['draws']}, losses: {team['losses']}, goals for: {team['goals_for']}, goals against: {team['goals_against']}, def: {deference_goals}, points: {team['points']}")

# task 6        
def best_team(sorted_teams):
    if not sorted_teams or sorted_teams[0]["played"] == 0:
        logging.warning("Attempted to get the best team, but no games have been played yet.")
        raise ValueError("There isn't best team yet")
    return sorted_teams[0]

# task 7 
def best_score_team(teams):
    played_teams = []
    for team in teams:
        if team["played"] > 0:
            played_teams.append(team)
    if not played_teams:
        raise ValueError("No games played yet.")
    max_goals = -1
    for team in played_teams:
        if team["goals_for"] > max_goals:
            max_goals = team["goals_for"]       
    best_teams = []
    for team in played_teams:
        if team["goals_for"] == max_goals:
            best_teams.append(team["name"])           
    return best_teams

# task 8
def success_percentage(team):
    if not team["played"]:
        logging.warning(f"Attempted success percentage for team ID {team['id']} with zero games played.")
        raise ValueError("No games")
    percent = team["points"] / (team["played"] * 3) * 100
    return percent

def get_team_by_id(teams, team_id):
    validate_id(team_id)
    id_val = int(team_id)
    for team in teams:
        if team["id"] == id_val:
            return team
    logging.warning(f"Team with ID {team_id} does not exist during lookup.")
    raise ValueError(f"Team with ID {team_id} does not exist.")

# task 9
def teams_not_win(teams):
    for team in teams:
        if team["played"] and team["wins"] == 0:
            print(f"Name: {team['name']}, Played: {team['played']} Points: {team['points']}")

# task 10
def calculate_tournament_summary(teams, matches):
    if not matches:
        logging.warning("Attempted to calculate tournament summary, but no matches exist.")
        raise ValueError("No matches!")
    num_of_teams = len(teams)
    num_of_matches = len(matches)
    num_of_goals = 0
    num_of_draws = 0
    for team in teams:
        num_of_goals += team["goals_for"]
        num_of_draws += team["draws"]
    num_of_draws /= 2
    avg_goals_match = round((num_of_goals / num_of_matches), 2)
    sorted_t = sort_teams(teams)
    the_best_team = best_team(sorted_t)
    return {
        "num_of_teams": num_of_teams,
        "num_of_matches": num_of_matches,
        "num_of_goals": num_of_goals,
        "avg_goals_match": avg_goals_match,
        "num_of_draws": num_of_draws,
        "leading_team": the_best_team['name']
    }

def show_tournament_summary(summary):
    print(f"Number of teams: {summary['num_of_teams']}")
    print(f"Number of matches: {summary['num_of_matches']}")
    print(f"Total goals: {summary['num_of_goals']}")
    print(f"Average goals per match: {summary['avg_goals_match']}")
    print(f"Number of draws: {summary['num_of_draws']}")
    print(f"Leading team: {summary['leading_team']}")

# main
def main():
    teams = []
    matches = []
    logging.info("Tournament manager system initialized.")
    while True:
        print("\n========== TOURNAMENT MANAGER ==========")
        print("1. Add team")
        print("2. Show all teams")
        print("3. Add match result")
        print("4. Show standings")
        print("5. Show leading team")
        print("6. Show best attacking team")
        print("7. Show team success rate")
        print("8. Show teams without wins")
        print("9. Show tournament summary")
        print("10. Check championship potential")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            logging.info("Tournament manager system closed by user.")
            break   
        elif choice == "1":
            try:
                id_input = input("Enter team ID (positive integer): ")
                name_input = input("Enter team name: ")
                add_team(teams, id_input, name_input)
                print("Team added successfully.")
            except ValueError as e:
                logging.warning(f"Menu option 1 failed: {e}")
                print(f"Error: {e}")       
        elif choice == "2":
            try:
                show_teams(teams)
            except ValueError as e:
                logging.warning(f"Menu option 2 failed: {e}")
                print(f"Error: {e}")        
        elif choice == "3":
            try:
                home_id = int(input("Enter home team ID: "))
                away_id = int(input("Enter away team ID: "))
                home_g = input("Enter home goals: ")
                away_g = input("Enter away goals: ")
                add_matches(teams, matches, home_id, away_id, home_g, away_g)
                print("Match result added and update details in teams.")
            except ValueError as e:
                logging.warning(f"Menu option 3 failed: {e}")
                print(f"Error: {e}")       
        elif choice == "4":
            try:
                sorted_teams_list = sort_teams(teams)
                show_sorted_teams(sorted_teams_list)
            except ValueError as e:
                logging.warning(f"Menu option 4 failed: {e}")
                print(f"Error: {e}")   
        elif choice == "5":
            try:
                sorted_teams_list = sort_teams(teams)
                leader = best_team(sorted_teams_list)
                print(f"Leading team: {leader['name']} with {leader['points']} points.")
            except ValueError as e:
                logging.warning(f"Menu option 5 failed: {e}")
                print(f"Error: {e}")
        elif choice == "6":
            try:
                best_teams_list = best_score_team(teams)
                print(f"Best attacking team(s): {best_teams_list}")
            except ValueError as e:
                logging.warning(f"Menu option 6 failed: {e}")
                print(f"Error: {e}")
        elif choice == "7":
            try:
                team_id_input = input("Enter team ID to check success rate: ")
                found_team = get_team_by_id(teams, team_id_input)
                rate = success_percentage(found_team)
                print(f"Success rate for {found_team['name']}: {rate:.2f}%")
            except ValueError as e:
                logging.warning(f"Menu option 7 failed: {e}")
                print(f"Error: {e}")  
        elif choice == "8":
            try:
                teams_not_win(teams)
            except ValueError as e:
                logging.warning(f"Menu option 8 failed: {e}")
                print(f"Error: {e}")
        elif choice == "9":
            try:
                summary = calculate_tournament_summary(teams, matches)
                show_tournament_summary(summary)
            except ValueError as e:
                logging.warning(f"Menu option 9 failed: {e}")
                print(f"Error: {e}")
        elif choice == "10":
            print("Championship potential option (Challenge task).")
        else:
            logging.warning(f"Invalid menu choice entered: {choice}")
            print("Invalid option. Please choose a number between 0 and 10.")

if __name__ == "__main__":
    main()