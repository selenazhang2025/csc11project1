"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate
an entire playthrough of the game. Please consult the project handout for
instructions and details.

You can copy/paste your code from Assignment 1 into this file, and modify it as
needed to work with your game.

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
from event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """
        Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands when starting from the location at initial_location_id
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)

        # Add first event (initial location, no previous command)
        initial_location = self._game.get_location()
        initial_event = Event(initial_location.id_num, initial_location.long_description)
        self._events.add_event(initial_event, None)

        # Generate the remaining events based on the commands and initial location
        if commands:
            self.generate_events(commands, initial_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """
        Generate events in this simulation, based on current_location and commands, a valid list of commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands when starting from current_location
        """
        for command in commands:
            # Handle puzzle solving - this unlocks new commands
            if command.startswith("solve "):
                parts = command.split()
                if len(parts) >= 2:
                    solution = parts[1]
                    success, _ = self._game.solve_puzzle(solution)
                    if success:
                        # Update current_location to reflect unlocked command
                        current_location = self._game.get_location()
                continue
            
            # Handle take and use commands - update game state but don't change location
            if command.startswith("take "):
                parts = command.split()
                if len(parts) >= 2:
                    item_name = parts[1]
                    self._game.take_item(item_name)
                continue
            
            if command.startswith("use "):
                parts = command.split()
                if len(parts) >= 2:
                    item_name = parts[1]
                    self._game.use_item(item_name)
                continue
            
            # Handle movement commands
            if command in current_location.available_commands:
                new_location_id = current_location.available_commands[command]
                self._game.current_location_id = new_location_id
                new_location = self._game.get_location()
                new_event = Event(new_location.id_num, new_location.long_description)
                self._events.add_event(new_event, command)
                current_location = new_location
            elif command in ["look", "inventory", "score", "log"]:
                # Menu commands don't change location, skip for simulation
                continue

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.
        """
        # Note: We have completed this method for you. Do NOT modify it for A1.

        return self._events.get_id_log()

    def run(self) -> None:
        """
        Run the game simulation and log location descriptions.
        """
        # Note: We have completed this method for you. Do NOT modify it for A1.

        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    # })

    # Win walkthrough: Complete path to win the game
    win_walkthrough = [
        "take usb_drive",  # Location 1
        "go east",  # Location 3
        "go north",  # Location 6
        "take project_file",  # Location 6
        "go south",  # Location 3
        "go west",  # Location 1
        "go west",  # Location 2
        "go up",  # Location 5
        "take laptop_charger",  # Location 5
        "go down",  # Location 2
        "go east",  # Location 1
        "go south",  # Location 4
        "go west",  # Location 8
        "solve 2511",  # Location 8 - solve puzzle
        "enter lab",  # Location 10
        "use usb_drive",  # Location 10
        "use project_file",  # Location 10
        "use laptop_charger"  # Location 10 - win condition
    ]
    expected_log = [1, 3, 6, 3, 1, 2, 5, 2, 1, 4, 8, 10]  # Location IDs visited
    sim = AdventureGameSimulation('game_data.json', 1, win_walkthrough)
    assert expected_log == sim.get_id_log()

    # Lose demo: Exceed maximum moves
    lose_demo = [
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west",  # Location 1
        "go east",  # Location 3
        "go west"  # Location 1 - exceeds max moves
    ]
    expected_log = [1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1]
    sim = AdventureGameSimulation('game_data.json', 1, lose_demo)
    assert expected_log == sim.get_id_log()

    # Inventory demo: Pick up items and check inventory
    inventory_demo = [
        "take usb_drive",  # Location 1
        "go east",  # Location 3
        "go north",  # Location 6
        "take project_file",  # Location 6
        "inventory",  # Check inventory
        "go south",  # Location 3
        "go west",  # Location 1
        "go west",  # Location 2
        "go up",  # Location 5
        "take laptop_charger",  # Location 5
        "inventory"  # Check inventory again
    ]
    expected_log = [1, 3, 6, 3, 1, 2, 5]
    sim = AdventureGameSimulation('game_data.json', 1, inventory_demo)
    assert expected_log == sim.get_id_log()

    # Score demo: Use items to gain points
    scores_demo = [
        "take usb_drive",  # Location 1
        "go east",  # Location 3
        "go south",  # Location 7
        "take coffee",  # Location 7
        "go north",  # Location 3
        "go west",  # Location 1
        "go south",  # Location 4
        "go west",  # Location 8
        "solve 2511",  # Solve puzzle
        "enter lab",  # Location 10
        "score",  # Check score
        "use coffee",  # Location 10 - gain 5 points
        "score"  # Check score again
    ]
    expected_log = [1, 3, 7, 3, 1, 4, 8, 10]
    sim = AdventureGameSimulation('game_data.json', 1, scores_demo)
    assert expected_log == sim.get_id_log()

    # Enhancement demo: Solve the logic puzzle
    enhancement1_demo = [
        "go south",  # Location 4
        "go west",  # Location 8 - puzzle location
        "solve 1234",  # Wrong code
        "solve 2511",  # Correct code - unlocks lab
        "enter lab"  # Location 10
    ]
    expected_log = [1, 4, 8, 10]
    sim = AdventureGameSimulation('game_data.json', 1, enhancement1_demo)
    assert expected_log == sim.get_id_log()

    # Note: You can add more code below for your own testing purposes
