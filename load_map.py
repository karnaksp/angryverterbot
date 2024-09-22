"""
Module for initialization game map.
"""
import json
from load_data import load_json

def init_start_location(start_id: int = 1, locations_file: str = 'info/locations.json') -> None:
    """
    Load the starting location when the game begins and reorder the JSON so that
    the starting location is first.

    Parameters
    ----------
    start_id : int
        The ID of the starting location.
    locations_file : str
        Path to the JSON file with locations.
    """
    locations_data = load_json(locations_file)
    if str(start_id) not in locations_data:
        raise ValueError(f"Starting location ID {start_id} is not found in the locations data.")
    
    start_location = locations_data.pop(str(start_id))
    locations_data = {str(start_id): start_location, **locations_data}
    with open(locations_file, 'w') as file:
        json.dump(locations_data, file, indent=4)

def load_map(locations_file: str = 'info/locations.json') -> dict:
    """
    Load the map data from a JSON file.

    Parameters
    ----------
    locations_file : str
        Path to the JSON file with locations.

    Returns
    -------
    dict
        Dictionary with locations data.
    """
    return load_json(locations_file)

if __name__ == "__main__":
    init_start_location()
    locations = load_map()
    print(locations)
