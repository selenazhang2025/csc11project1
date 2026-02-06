"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2026 CSC111 Teaching Team
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: The unique identifier for this location
        - brief_description: A short description shown when revisiting this location
        - long_description: A detailed description shown when first visiting this location
        - available_commands: A dictionary mapping command strings to location IDs they lead to
        - items: A list of item names that are present at this location
        - visited: Whether this location has been visited before
        - puzzle: Optional dictionary containing puzzle information (if this location has a puzzle)
        - is_submission_location: Whether this location allows project submission

    Representation Invariants:
        - id_num > 0
        - All values in available_commands are valid location IDs
        - All strings in items are valid item names
    """

    id_num: int
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: list[str]
    visited: bool = False
    puzzle: Optional[dict] = None
    is_submission_location: bool = False


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: The name of the item
        - description: A description of what the item is
        - start_position: The location ID where this item can be found
        - target_position: The location ID where this item can be used
        - target_points: The number of points awarded when using this item at its target location

    Representation Invariants:
        - start_position > 0
        - target_position > 0
        - target_points >= 0
    """

    name: str
    description: str
    start_position: int
    target_position: int
    target_points: int


# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.

if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    # })
