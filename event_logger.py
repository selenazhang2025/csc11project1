"""CSC111 Project 1: Text Adventure Game - Event Logger

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

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
from dataclasses import dataclass
from typing import Optional


@dataclass
class Event:
    """
    A node representing one event in an adventure game.

    Instance Attributes:
    - id_num: Integer id of this event's location
    - description: Long description of this event's location
    - next_command: String command which leads this event to the next event, None if this is the last game event
    - next: Event object representing the next event in the game, or None if this is the last game event
    - prev: Event object representing the previous event in the game, None if this is the first game event
    """
    id_num: int
    description: str
    next_command: Optional[str] = None
    next: Optional[Event] = None
    prev: Optional[Event] = None


class EventList:
    """
    A linked list of game events.

    Instance Attributes:
        - first: The first Event in the linked list, or None if the list is empty
        - last: The last Event in the linked list, or None if the list is empty

    Representation Invariants:
        - If the list is empty, both first and last are None
        - If the list is not empty, first.prev is None and last.next is None
    """
    first: Optional[Event]
    last: Optional[Event]

    def __init__(self) -> None:
        """Initialize a new empty event list."""

        self.first = None
        self.last = None

    def display_events(self) -> None:
        """Display all events in chronological order."""
        if self.is_empty():
            print("No events logged yet.")
            return
        curr = self.first
        event_num = 1
        while curr:
            if curr.next_command is not None:
                print(f"Event {event_num}: Location {curr.id_num}, Command: {curr.next_command}")
            else:
                print(f"Event {event_num}: Location {curr.id_num} (Starting location)")
            curr = curr.next
            event_num += 1

    def is_empty(self) -> bool:
        """Return whether this event list is empty."""
        return self.first is None

    def add_event(self, event: Event, command: str = None) -> None:
        """
        Add the given new event to the end of this event list.
        The given command is the command which was used to reach this new event, or None if this is the first
        event in the game.
        """
        if self.is_empty():
            self.first = event
            self.last = event
            event.prev = None
            event.next = None
            event.next_command = None
        else:
            # Update the previous last event's next_command and next
            if self.last is not None:
                self.last.next_command = command
                self.last.next = event
            event.prev = self.last
            event.next = None
            event.next_command = None
            self.last = event

    def remove_last_event(self) -> None:
        """
        Remove the last event from this event list.
        If the list is empty, do nothing.
        """
        if self.is_empty():
            return

        if self.first == self.last:
            # Only one event in the list
            self.first = None
            self.last = None
        else:
            # Update the new last event
            if self.last is not None and self.last.prev is not None:
                self.last.prev.next = None
                self.last.prev.next_command = None
                self.last = self.last.prev

    def get_id_log(self) -> list[int]:
        """Return a list of all location IDs visited for each event in this list, in sequence."""
        result = []
        current = self.first
        while current is not None:
            result.append(current.id_num)
            current = current.next
        return result

    # Note: You may add other methods to this class as needed


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    # })
