"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2026 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional

from game_entities import Location, Item
from event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: The ID of the player's current location
        - ongoing: Whether the game is still in progress
        - inventory: A list of item names the player is currently carrying
        - score: The player's current score
        - moves: The number of moves the player has made
        - max_moves: The maximum number of moves allowed before losing
        - submission_required_items: A list of item names required to submit the project

    Representation Invariants:
        - current_location_id > 0 and current_location_id is a valid location ID
        - score >= 0
        - moves >= 0
        - max_moves > 0
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]

    # Public game state
    current_location_id: int
    ongoing: bool
    inventory: list[str]
    score: int
    moves: int
    max_moves: int
    submission_required_items: list[str]
    used_items: set[str]

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Load game data
        self._locations, self._items, self.max_moves, self.submission_required_items = (
            self._load_game_data(game_data_file)
        )

        # Initialize game state
        self.current_location_id = initial_location_id
        self.ongoing = True
        self.inventory = []
        self.score = 0
        self.moves = 0

        # Track which items have been used (prevents re-using an item for infinite points)
        self.used_items = set()

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item], int, list[str]]:
        """Load locations and items from a JSON file with the given filename and return:
        (1) a dictionary mapping location IDs to Location objects,
        (2) a list of all Item objects,
        (3) the maximum number of moves allowed, and
        (4) the list of required items for submission.
        """

        with open(filename, 'r') as f:
            data = json.load(f)

        locations = {}
        for loc_data in data['locations']:
            loc_id = loc_data['id']
            location_obj = Location(
                loc_id,
                f"LOCATION {loc_id}\n{loc_data['brief_description']}",
                f"LOCATION {loc_id}\n{loc_data['long_description']}",
                loc_data['available_commands'],
                loc_data['items'],
                visited=False,
                puzzle=loc_data.get('puzzle'),
                is_submission_location=loc_data.get('is_submission_location', False)
            )
            locations[loc_id] = location_obj

        items = []
        for item_data in data['items']:
            item_obj = Item(
                item_data['name'],
                item_data['description'],
                item_data['start_position'],
                item_data['target_position'],
                item_data['target_points']
            )
            items.append(item_obj)

        max_moves = data.get('max_moves', 50)
        submission_required_items = data.get('submission_required_items', [])

        return locations, items, max_moves, submission_required_items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """
        if loc_id is None:
            loc_id = self.current_location_id
        return self._locations[loc_id]

    def get_item_by_name(self, name: str) -> Optional[Item]:
        """Return the Item object with the given name, or None if no such item exists."""
        for game_item in self._items:
            if game_item.name == name:
                return game_item
        return None

    def take_item(self, item_name1: str) -> str:
        """Attempt to take an item from the current location.
        Returns a message describing the result.
        """
        item_location = self.get_location()

        if item_name1 not in item_location.items:
            return f"There is no '{item_name1}' here."

        if item_name1 in self.inventory:
            return f"You already have the {item_name1}."

        self.inventory.append(item_name1)
        item_location.items.remove(item_name1)
        return f"You picked up the {item_name1}."

    def use_item(self, item_name2: str) -> str:
        """Attempt to use an item at the current location.
        Returns a message describing the result.
        """
        if item_name2 not in self.inventory:
            return f"You don't have the {item_name2}."

        if item_name2 in self.used_items:
            return f"You already used the {item_name2}."

        item1 = self.get_item_by_name(item_name2)
        if item1 is None:
            return f"Unknown item: {item_name2}."

        location1 = self.get_location()

        if item1.target_position != location1.id_num:
            return f"You can't use the {item_name2} here. It needs to be used at location {item1.target_position}."

        # Item is used successfully
        self.score += item1.target_points
        self.used_items.add(item_name2)
        return f"You used the {item_name2}! You gained {item1.target_points} points."

    def solve_puzzle(self, solution: str) -> tuple[bool, str]:
        """Attempt to solve a puzzle at the current location.
        Returns a tuple (success, message).
        """
        location2 = self.get_location()

        if location2.puzzle is None:
            return False, "There is no puzzle here."

        correct_solution = location2.puzzle.get('solution')

        if solution == correct_solution:
            unlocks_location = location2.puzzle.get('unlocks_location')
            if unlocks_location:
                location2.available_commands['enter lab'] = unlocks_location
                return True, "Correct! The door unlocks. You can now 'enter lab'."
            return True, "Correct!"
        return False, "That's not the correct code. Try again!"

    def check_win_condition(self) -> bool:
        """Check if the player has won the game.
        Player wins by being at the submission location with all required items.
        """
        location3 = self.get_location()

        if not location3.is_submission_location:
            return False

        # Check if player has all required items
        for required_item in self.submission_required_items:
            if required_item not in self.inventory:
                return False

        return True

    def check_lose_condition(self) -> bool:
        """Check if the player has lost the game.
        Player loses if they exceed the maximum number of moves.
        """
        return self.moves >= self.max_moves

    def move_to_location(self, new_location_id1: int) -> None:
        """Move the player to a new location and update game state."""
        self.current_location_id = new_location_id1
        self.moves += 1

        # Check lose condition
        if self.check_lose_condition():
            self.ongoing = False
            return

        # Check win condition
        if self.check_win_condition():
            self.ongoing = False
            return


def _print_items_at_location(helper_game: AdventureGame, helper_location: Location) -> None:
    """Print items at a location (if any)."""
    if not helper_location.items:
        return

    print("\nItems here:")
    for item_name0 in helper_location.items:
        item0 = helper_game.get_item_by_name(item_name0)
        if item0 is not None:
            print(f"  - {item_name0}: {item0.description}")


def _print_inventory(helper_game2: AdventureGame) -> None:
    """Print the player's inventory."""
    if not helper_game2.inventory:
        print("\nYour inventory is empty.")
        return

    print("\nYour inventory:")
    for item_name02 in helper_game2.inventory:
        item02 = helper_game2.get_item_by_name(item_name02)
        if item02 is not None:
            print(f"  - {item_name02}: {item02.description}")


def handle_menu_command(game_menu: AdventureGame, game_log_menu: EventList, command: str) -> None:
    """Handle menu commands that don't change location."""
    if command == "look":
        location0 = game_menu.get_location()
        print("\n" + "=" * 50)
        print(location0.long_description)
        _print_items_at_location(game_menu, location0)
        print("=" * 50)
        return

    if command == "inventory":
        _print_inventory(game_menu)
        return

    if command == "score":
        print(f"\nYour current score: {game_menu.score} points")
        print(f"Moves remaining: {game_menu.max_moves - game_menu.moves}")
        return

    if command == "log":
        print("\nEvent Log:")
        game_log_menu.display_events()
        return

    if command == "quit":
        print("\nThanks for playing! Goodbye.")
        game_menu.ongoing = False


def handle_take_command(game1: AdventureGame, command: str) -> str:
    """Handle 'take [item]' command."""
    parts = command.split()
    if len(parts) < 2:
        return "Take what? Use 'take [item name]'"
    item_name5 = parts[1]
    return game1.take_item(item_name5)


def handle_use_command(game2: AdventureGame, command: str) -> str:
    """Handle 'use [item]' command."""
    parts = command.split()
    if len(parts) < 2:
        return "Use what? Use 'use [item name]'"
    item_name6 = parts[1]
    return game2.use_item(item_name6)


def handle_solve_command(game3: AdventureGame, command: str) -> tuple[bool, str]:
    """Handle 'solve [code]' command for puzzles."""
    parts = command.split()
    if len(parts) < 2:
        return False, "Solve what? Use 'solve [code]'"
    solution = parts[1]
    return game3.solve_puzzle(solution)


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'R0902', 'E9998', 'E9999', 'static_type_checker']
    # })

    print("=" * 60)
    print("CSC111 PROJECT SUBMISSION ADVENTURE")
    print("=" * 60)
    print("You and your friend finished your CS project yesterday!")
    print("But there's a bug that needs fixing before the 1pm deadline.")
    print("Find the items you need, solve the puzzle, and submit your project!")
    print("=" * 60)
    print()

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "log", "quit"]  # Regular menu options available at each location
    choice = None

    # Add initial event
    initial_location = game.get_location()
    initial_event = Event(initial_location.id_num, initial_location.long_description)
    game_log.add_event(initial_event, None)

    while game.ongoing:
        location = game.get_location()

        # Display location description
        print("\n" + "=" * 60)
        if not location.visited:
            print(location.long_description)
            location.visited = True
        else:
            print(location.brief_description)

        # Show items at this location
        if location.items:
            print("\nYou see:")
            for item_name in location.items:
                item = game.get_item_by_name(item_name)
                if item:
                    print(f"  - {item_name}: {item.description}")

        # Show puzzle hint if there's a puzzle
        if location.puzzle and 'enter lab' not in location.available_commands:
            print(f"\n{location.puzzle.get('hint', 'There is a puzzle here.')}")

        print("=" * 60)

        # Display possible actions
        print("\nWhat to do?")
        print("Menu commands: look, inventory, score, log, quit")
        print("Item commands: take [item], use [item]")
        if location.puzzle and 'enter lab' not in location.available_commands:
            print("Puzzle command: solve [code]")
        print("\nAt this location, you can also:")
        for action in location.available_commands:
            print(f"  - {action}")

        # Get user input
        choice = input("\nEnter action: ").lower().strip()

        # Handle special commands
        if choice.startswith("take "):
            result = handle_take_command(game, choice)
            print(f"\n{result}")
            continue
        elif choice.startswith("use "):
            result = handle_use_command(game, choice)
            print(f"\n{result}")
            # Check win condition after using item
            if game.check_win_condition():
                print("\n" + "=" * 60)
                print("CONGRATULATIONS! You've successfully submitted your project!")
                print(f"Final Score: {game.score} points")
                print(f"Moves used: {game.moves}/{game.max_moves}")
                print("=" * 60)
                game.ongoing = False
            continue
        elif choice.startswith("solve "):
            success, message = handle_solve_command(game, choice)
            print(f"\n{message}")
            continue

        # Validate choice for regular commands
        valid_commands = list(location.available_commands.keys()) + menu
        while choice not in valid_commands:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("\n" + "=" * 60)
        print(f"You decided to: {choice}")
        print("=" * 60)

        if choice in menu:
            handle_menu_command(game, game_log, choice)
        else:
            # Handle movement commands
            if choice in location.available_commands:
                new_location_id = location.available_commands[choice]
                game.move_to_location(new_location_id)

                # Add event to log
                new_location = game.get_location()
                new_event = Event(new_location.id_num, new_location.long_description)
                game_log.add_event(new_event, choice)

                # Check win/lose conditions
                if game.check_win_condition():
                    print("\n" + "=" * 60)
                    print("CONGRATULATIONS! You've successfully submitted your project!")
                    print(f"Final Score: {game.score} points")
                    print(f"Moves used: {game.moves}/{game.max_moves}")
                    print("=" * 60)
                    game.ongoing = False
                elif game.check_lose_condition():
                    print("\n" + "=" * 60)
                    print("GAME OVER!")
                    print("You've run out of moves. The deadline has passed.")
                    print(f"Final Score: {game.score} points")
                    print("=" * 60)
                    game.ongoing = False

    # Final message
    if not game.ongoing:
        print("\nThanks for playing!")
