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