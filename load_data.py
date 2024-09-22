"""
Module for initialization start state for other roles.
"""

import json
import random
from roles import Protagonist, NPC, Verter
from typing import Dict, List, Any


def load_json(file_name: str) -> Dict:
    """
    Load JSON data from a file.

    Parameters
    ----------
    file_name : str
        The path to the JSON file.

    Returns
    -------
    dict
        The data loaded from the JSON file.
    """
    with open(file_name, "r") as file:
        return json.load(file)


def initialize_player(
    name="CatPlayer", item="Head & Shoulders", id="001"
) -> "Protagonist":
    """
    Initialize the protagonist with a default profile.

    Returns
    -------
    Protagonist
        The initialized protagonist object.
    """
    return Protagonist(name, item, id)


def initialize_npcs(
    name_npcs: List[str],
    types_npcs: List[str],
    quests: Dict[str, Dict[str, Any]],
    locations: List[Dict[str, Any]],
    phrases: List[str],
    items: List[Dict[str, Any]],
) -> List[NPC]:
    """
    Initialize a list of NPCs, distributed across all locations.

    Parameters
    ----------
    num_npcs : int
        The total number of NPCs to create.
    name_npcs: list
        List of names NPCs can have.
    type_npcs: list
        List of types NPCs can have.
    quests: dict
        Dictionary of quests that the NPCs can give.
    locations: list
        List of location dictionaries that NPCs can be assigned to.
    phrases: list
        List of phrases that NPCs can say.
    items: list
        Items that are in NPC's inventory.

    Returns
    -------
    list
        List of initialized NPC objects.
    """
    npcs = []

    for _, loc_details in locations.items():
        loc_name = loc_details["name"]
        num_npcs_for_location = random.randint(1, 3)

        for _ in range(num_npcs_for_location):
            npcs.append(
                NPC(
                    name=random.choice(name_npcs),
                    type=random.choice(types_npcs),
                    quests=quests,
                    location=loc_name,
                    phrases=phrases,
                    inventory=items,
                )
            )

    return npcs


def initialize_verters(
    projects: Dict[str, Dict[str, Any]],
    verter_phrases: List[str],
    locations: Dict[str, Dict[Any, Any]],
) -> List["Verter"]:
    """
    Initialize a list of Verter enemies based on the projects.

    Parameters
    ----------
    projects : dict
        Dictionary of project-based quests.
    verter_phrases : list
        List of phrases that the Verters can say.
    locations : list
        List of available locations with their IDs.

    Returns
    -------
    list
        List of initialized Verter objects.
    """
    return [
        Verter(
            {**project, "name": key},
            locations.get(project["location_id"], {}).get("name", "WTF Location"),
            verter_phrases,
        )
        for key, project in projects.items()
    ]


def init_game_elements(
    name_player: str = "CatPlayer", item: str = "Head & Shoulders"
) -> None:
    """
    Main function to initialize the game state.

    Parameters
    ----------
    num_npcs : int
        Number of npcs to initialize.
    """
    global items, quests, projects, locations
    items = load_json("info/items.json")
    phrases = load_json("info/phrases.json")
    quests = load_json("info/quests.json")
    projects = {
        key: value
        for key, value in quests.items()
        if "type" in value and value["type"] == "project"
    }
    locations = load_json("info/locations.json")
    name_npcs = [
        "Meow, Booba",
        "Odsi Whish",
        "Ymir Fritz",
        "Mario",
        "Bowser",
        "Sakura",
        "Nana",
        "Karnaks Puck",
        "Fry",
        "Basic",
        "Johnny Silverhand",
        "V",
        "Bender Rodriges",
        "Sif",
        "Belmont",
    ]
    types_npcs = ["Peer", "ADM", "Other"]

    player: Protagonist = initialize_player(name_player, item)

    verters: List[Verter] = initialize_verters(
        projects, phrases["verter_phrases"], locations
    )

    npcs: List["NPC"] = initialize_npcs(
        name_npcs,
        types_npcs,
        quests,
        locations,
        phrases["peer_phrases"],
        items["items"],
    )

    return player, verters, npcs


if __name__ == "__main__":
    init_game_elements()
