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
