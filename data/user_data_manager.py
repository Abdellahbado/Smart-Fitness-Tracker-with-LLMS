import json
import os

WORKOUT_PLANS_FILE = "data/workout_plans.json"
NUTRITION_PLANS_FILE = "data/nutrition_plans.json"
PERSONALIZED_WORKOUTS_FILE = "data/personalized_workouts.json"


def load_data(file_name, username):
    try:
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                try:
                    all_data = json.load(f)
                    print(f"Loaded data from {file_name} for user {username}: {all_data.get(username, [])}")
                    return all_data.get(username, [])
                except json.JSONDecodeError:
                    print(f"Empty or malformed JSON in {file_name}. Returning empty list.")
                    return []
    except Exception as e:
        print(f"Error loading data from {file_name}: {e}")
    return []


def save_data(file_name, username, data):
    all_data = {}
    try:
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                try:
                    all_data = json.load(f)
                except json.JSONDecodeError:
                    print(f"Empty or malformed JSON in {file_name}. Initializing with empty dict.")
                    all_data = {}

        if username not in all_data:
            all_data[username] = []

        all_data[username].append(data)

        with open(file_name, "w") as f:
            json.dump(all_data, f, indent=4)
        print(f"Saved data to {file_name} for user {username}: {data}")
    except Exception as e:
        print(f"Error saving data to {file_name}: {e}")


def save_workout_plan(username, workout_plan):
    save_data(WORKOUT_PLANS_FILE, username, workout_plan)


def load_workout_plan(username):
    return load_data(WORKOUT_PLANS_FILE, username)


def save_nutrition_plan(username, nutrition_plan):
    save_data(NUTRITION_PLANS_FILE, username, nutrition_plan)


def load_nutrition_plan(username):
    return load_data(NUTRITION_PLANS_FILE, username)


def save_personalized_workout(username, personalized_workout):
    save_data(PERSONALIZED_WORKOUTS_FILE, username, personalized_workout)


def load_personalized_workout(username):
    return load_data(PERSONALIZED_WORKOUTS_FILE, username)


# Example usage
