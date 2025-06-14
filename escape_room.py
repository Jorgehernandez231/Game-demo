# --- Define items and rooms ---

couch = {"name": "couch", "type": "furniture"}
piano = {"name": "piano", "type": "furniture"}
queenbed = {"name": "queenbed", "type": "furniture"}
doublebed = {"name": "doublebed", "type": "furniture"}
dresser = {"name": "dresser", "type": "furniture"}
dining_table = {"name": "dining table", "type": "furniture"}

door_a = {"name": "door a", "type": "door"}
door_b = {"name": "door b", "type": "door"}
door_c = {"name": "door c", "type": "door"}
door_d = {"name": "door d", "type": "door"}

key_a = {"name": "key for door a", "type": "key", "target": door_a}
key_b = {"name": "key for door b", "type": "key", "target": door_b}
key_c = {"name": "key for door c", "type": "key", "target": door_c}
key_d = {"name": "key for door d", "type": "key", "target": door_d}

gameroomlight = {"name": "gameroomlight", "type": "light"}
bedroom_1_light = {"name": "bedroom1light", "type": "light"}
bedroom_2_light = {"name": "bedroom2light", "type": "light"}
livingroom_light = {"name": "livingroomlight", "type": "light"}

game_room = {"name": "game room", "type": "room"}
bedroom_1 = {"name": "bedroom 1", "type": "room"}
bedroom_2 = {"name": "bedroom 2", "type": "room"}
living_room = {"name": "living room", "type": "room"}
outside = {"name": "outside", "type": "room"}

# --- Object relations ---
object_relations = {
    "game room": [couch, piano, door_a, gameroomlight],
    "piano": [key_a],
    "queenbed": [key_b],
    "bedroom 1": [queenbed, door_b, door_c, door_a, bedroom_1_light],
    "bedroom 2": [dresser, doublebed, door_b, bedroom_2_light],
    "doublebed": [key_c],
    "dresser": [key_d],
    "living room": [door_d, door_c, dining_table, livingroom_light],
    "outside": [door_d],
    "door a": [game_room, bedroom_1],
    "door b": [bedroom_1, bedroom_2],
    "door c": [bedroom_1, living_room],
    "door d": [living_room, outside],
}

# --- Initial game state ---
INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside,
    "rooms_with_light_on": []
}

# --- Game logic functions ---
def linebreak():
    print("\n\n")

def start_game(game_state):
    print("You wake up on a couch and find yourself in a strange house with no windows and no lights...")
    play_room(game_state["current_room"], game_state)
    

def play_room(room, game_state):
    game_state["current_room"] = room
    explore_light(room, game_state)

    if room == game_state["target_room"]:
        print("Congrats! You escaped the house!")
        return

    print("You are now in " + room["name"])
    action = input("What would you like to do? Type 'explore' or 'examine': ").strip().lower()

    if action == "explore":
        explore_room(room, game_state)
        play_room(room, game_state)
    elif action == "examine":
        examine_item(input("What would you like to examine? ").strip())
    else:
        print("Not sure what you mean.")
        play_room(room, game_state)
    linebreak()

def explore_light(room, game_state):
    room_name = room["name"]
    if room_name in game_state["rooms_with_light_on"]:
        return  # Light already on

    light = next((item for item in object_relations[room_name] if item["type"] == "light"), None)
    if light:
        action = input(f"The room is dark. Do you want to turn on the {light['name']}? (yes/no): ").strip().lower()
        if action == "yes":
            print(f"You turned on the {light['name']}.")
            game_state["rooms_with_light_on"].append(room_name)
        else:
            print("You need to turn on the light first to explore the room.")
            play_room(room, game_state)

def explore_room(room):
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You explore the room. This is " + room["name"] + ". You find: " + ", ".join(items))

def get_next_room_of_door(door, current_room):
    connected_rooms = object_relations[door["name"]]
    return connected_rooms[1] if connected_rooms[0] == current_room else connected_rooms[0]

def examine_item(item_name, game_state):
    current_room = game_state["current_room"]
    next_room = None
    output = None

    for item in object_relations[current_room["name"]]:
        if item["name"].lower() == item_name.lower():
            output = f"You examine {item_name}. "
            if item["type"] == "door":
                has_key = any(key["target"] == item for key in game_state["keys_collected"])
                if has_key:
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "It's locked. You don't have the key."
            else:
                if item["name"] in object_relations and object_relations[item["name"]]:
                    found_item = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(found_item)
                    output += f"You find {found_item['name']}."
                else:
                    output += "There is nothing interesting."
            print(output)
            break

    if output is None:
        print("The item is not found in this room.")

    if next_room:
        go = input("Do you want to go to the next room? (yes/no): ").strip().lower()
        if go == "yes":
            play_room(next_room, game_state)
        else:
            play_room(current_room, game_state)
    else:
        play_room(current_room, game_state)

# --- Start the game ---
