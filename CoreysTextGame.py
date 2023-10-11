# Corey Robbins

# Globals
# All the different themes for the game. theme[0] and theme[7] must be different or the game ends immediately.
# Sequel: Move themes into an external file to import them
Themes = [
    # Generic
    [
        # Rooms
        'West', 'Center', 'North', 'North-east',
        'South', 'South-east', 'East', 'East-north',
        # Items
        'Item Center', 'Item North', 'Item North-East', 'Item South', 'Item South-East', 'Item East',
        # Enemy name
        'Enemy',
        # Player approaches the enemy
        'The enemy is behind the {} door.',
        # Player has all items
        "You have all the items and will win.",
        # Player does not have all items
        "You're unprepared and will lose.",
        # Winning message
        'You win.',
        # Losing message
        'You lose.'
    ],
    # Space
    [
        # Rooms
        'Bridge', 'Crew Quarters', 'Science Facility', 'Hydroponics Module',
        'Engineering Center', 'Engines', 'Cargo Hold', 'Airlock',
        # Items
        'Medical Scanner', 'Plasma Emitter', 'Oxygen Mask', 'Plasma Coil', 'Plasma Charge', 'Armored Suit',
        # Enemy name
        'Alien',
        # Player approaches the enemy
        "You hear low, menacing sounds coming from the {} door.",
        # Player has all items
        "Whatever it is behind that door, you think you're ready to face it.",
        # Player does not have all items
        "It makes your knees shake with fear, going in there unprepared would be a death sentence.",
        # Winning message
        "Feeling confident and fully equipped, you walk into the airlock and quickly dispatch\n"
        "the creature that injured the crew. Congratulations, you win. Thanks for playing.",
        # Losing message
        "You wander into the airlock and stand face to face with the creature that injured the ship's crew.\n"
        "Unfortunately, you are woefully unprepared and very quickly join them. Sorry, you lose. Thanks for playing."
    ],
    # Blank
    [
        # Rooms
        'Start', '', '', '',
        '', '', '', 'Exit',
        # Items
        '', '', '', '', '', '',
        # Enemy name
        '',
        # Player approaches the enemy
        '',
        # Player has all items
        '',
        # Player does not have all items
        '',
        # Winning message
        '',
        # Losing message
        ''
    ]
]
# Select the theme here. This could be selected from a command line instead
theme = Themes[1]
# Use the room names from the theme to build the map
Rooms = {
    theme[0]: {                   'East': theme[1]},
    theme[1]: {'North': theme[2], 'East': theme[6], 'South': theme[4], 'West': theme[0], 'Item': theme[8]},
    theme[2]: {                   'East': theme[3], 'South': theme[1],                   'Item': theme[9]},
    theme[3]: {                                                        'West': theme[2], 'Item': theme[10]},
    theme[4]: {'North': theme[1], 'East': theme[5],                                      'Item': theme[11]},
    theme[5]: {                                                        'West': theme[4], 'Item': theme[12]},
    theme[6]: {'North': theme[7],                                      'West': theme[1], 'Item': theme[13]},
    theme[7]: {                                     'South': theme[6],                   'Item': theme[14]},

}
# Define keywords according to the theme
current_room = theme[0]
exit_room = theme[7]
enemy = theme[14]
win_message = theme[18]
lose_message = theme[19]
# The framework could actually be expanded to include diagonals like 'Northeast', or even multiple levels like 'Down'
ValidDirs = ['North', 'East', 'South', 'West']
inventory = []


def an(txt):
    """ Formats intelligent use of an or a before an object, such as an apple or a pear """
    if txt == '':
        # Blank
        return ''
    if txt[0].lower() in ['a', 'e', 'i', 'o', 'u', '8']:
        # Use 'an' when the first letter is a vowel
        return f' an {txt}'
    else:
        # Use 'a' when it is not
        return f' a {txt}'


def flist(lst, conj='and'):
    """ Formats ['A', 'B', 'C'] into 'A, B, and C' """
    length = len(lst)
    if length == 0:
        # Blank
        return ''
    elif length == 1:
        # Barely a list, just one item
        return lst[0]
    elif length == 2:
        # No need for commas yet
        return f'{lst[0]} {conj} {lst[1]}'
    else:
        # Make a full comma separated list
        return f'{", ".join(lst[:-1])}, {conj} {lst[-1]}'


def show_instructions():
    """ Prints an intro to the game """
    print(enemy, "Text Adventure Game by Corey Robbins")
    print(f"Collect 6 items to win the game, or be eaten by the {enemy.lower()}.")
    print("Move commands: go South, go North, go East, go West")
    print("Add to Inventory: get 'item name'")


def show_status():
    """ Prints the current room, any items or doors available, and the current inventory """
    # You are here
    print(f"\nYou are currently in the {current_room}.")
    if 'Item' in Rooms[current_room]:
        # There is an item on the ground in front of you
        print(f'There is{an(Rooms[current_room]["Item"])} on the ground here.')
    # Check for the available doors
    doors_list = [door for door in Rooms[current_room] if door in ValidDirs]
    # Pluralize and format the list properly
    print('There', 'is a door' if len(doors_list) == 1 else 'are doors', 'to the', flist(doors_list), end='.\n')
    for door in doors_list:
        # Check each door
        if Rooms[Rooms[current_room][door]].get('Item', '') == enemy:
            # The enemy is beyond this door
            print(theme[15].format(door))
            if len(inventory) == 6:
                # The player has all the items
                print(theme[16])
            else:
                # The player does not have all the items
                print(theme[17])
    if len(inventory) > 0:
        # List the player's inventory
        print(f'You have the {flist(inventory)}.')


def go(direction):
    """ Moves from room to room, with the necessary validation """
    # Moving requires changing the current room
    global current_room
    if direction not in ValidDirs:
        # You're giving me nonsense, try again
        print('Where are you trying to go? Pick an actual direction please.')
        return
    if direction in Rooms[current_room]:
        # If you find a door, go through it
        current_room = Rooms[current_room][direction]
    else:
        # If not, then don't
        print("There's nothing in that direction but solid wall!")


def get(item):
    """ Picks up an item and adds it to the inventory"""
    # print(f' get "{item}"')
    if 'Item' in Rooms[current_room]:
        # You find an item
        item_here = Rooms[current_room].get('Item', None)
        # This allows picking up whatever is in the room just by typing 'get'
        if item == '':
            item = item_here
        # print(f"Let's get {an(item)}.")
        # You don't have to type out the full name, just any part of it
        if item in item_here:
            # Pick the item up off the floor and put it in your inventory
            item = Rooms[current_room].pop('Item', 'ERROR')
            print(f'You picked up{an(item)}!')
            inventory.append(item)
        else:
            print(f"You see something on the ground, but it's not{an(item)}.")
    else:
        print("You don't see anything like that here.")


def main():
    """ The main game loop """
    # Play the intro movie
    show_instructions()
    # Keep playing until you're not
    while current_room != exit_room:
        # Prints the current room, any items or doors available, and the current inventory
        show_status()
        # Clear the input buffer
        inp = []
        # Ignore blank inputs, they break the game
        while not inp:
            # Get the input as a list of words
            inp = input('What is your command? ').split()
        # The first word is the verb such as go or get, the rest of the words make up the direction or item name
        verb, obj = inp[0].lower(), ' '.join(inp[1:])
        # Move to another room
        if verb == 'go':
            go(obj.title())
        # You can also just type the direction by itself, the go is implied
        elif verb.title() in ValidDirs:
            go(verb.title())
        # Pick up an item
        elif verb == 'get':
            get(obj.title())
        # You can just leave any time you want
        elif verb in ['exit', 'quit']:
            print("Goodbye!")
            return
        # Do I look like I know how to 'pick' an 'up the sword'? Go and Get only for now
        else:
            print(f"I don't understand how to {verb}{an(obj)}.")

    # You finished the game and broke out of the loop
    print()
    if len(inventory) == 6:
        # Congratulations, you win
        print(win_message)
    else:
        # Too bad, you lose
        print(lose_message)

    print("Goodbye!")


# Begin the main game loop
main()
