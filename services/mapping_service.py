import datetime
import os
import typing
from typing import Any, Dict, List, Optional, Union, cast

import googlemaps
from langchain_core.tools import BaseTool, tool

GMAPS_API_KEY = os.getenv("GMAPS_API_KEY")

client = googlemaps.Client(key=GMAPS_API_KEY)


def get_directions(
    origin: Union[str, Dict[str, Any], List],
    destination: Union[str, Dict[str, typing.Any], List],
    mode: Optional[str] = None,
    waypoints: Optional[Union[List, str]] = None,
    alternatives: bool = False,
    avoid: Optional[Union[List, str]] = None,
    language: Optional[str] = None,
    units: Optional[str] = None,
    region: Optional[str] = None,
    departure_time: Optional[Union[int, "datetime.datetime"]] = None,
    arrival_time: Optional[Union[int, "datetime.datetime"]] = None,
    optimize_waypoints: bool = False,
    transit_mode: Optional[Union[str, List[str]]] = None,
    transit_routing_preference: Optional[str] = None,
    traffic_model: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Get directions between an origin point and a destination point using specified travel mode and conditions.
    Parameters are passed directly to the Google Maps API client for flexible route querying.
    """
    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "waypoints": waypoints,
        "alternatives": alternatives,
        "avoid": avoid,
        "language": language,
        "units": units,
        "region": region,
        "departure_time": departure_time,
        "arrival_time": arrival_time,
        "optimize_waypoints": optimize_waypoints,
        "transit_mode": transit_mode,
        "transit_routing_preference": transit_routing_preference,
        "traffic_model": traffic_model,
    }
    # Filter out None values
    filtered_params = {key: value for key, value in params.items() if value is not None}
    return client.directions(**filtered_params)


def simple_directions(
    origin: str, destination: str, mode: Optional[str] = "driving"
) -> List[Dict[str, Any]]:
    """
    Provides a simplified method to get directions between two points with optional mode of transport.
    Defaults to driving mode if not specified.
    """
    return get_directions(origin, destination, mode=mode)


@tool
def get_walking_directions(origin: str, destination: str) -> List[Dict[str, Any]]:
    """
    Get walking directions between two points specified by `origin` and `destination`.
    """

    return get_directions(origin, destination, mode="walking")


@tool
def get_bicycling_directions(origin: str, destination: str) -> List[Dict[str, Any]]:
    """
    Get bicycling directions between two points specified by `origin` and `destination`.
    """

    return get_directions(origin, destination, mode="bicycling")


@tool
def get_transit_directions(origin: str, destination: str) -> str:
    """
    Get transit directions between two points specified by `origin` and `destination`,
    optionally using a specific `departure_time`.
    """

    directions = get_directions(origin, destination, mode="transit")[0]

    directions = remove_keys(
        directions,
        [
            "polyline",
            "url",
            "icon",
            "overview_polyline",
            "local_icon",
            "end_location",
            "start_location",
            "building_level",
            "bounds",
            "copyrights",
            "color",
            "text_color",
            "phone",
            "lat",
            "lng",
            "time_zone",
            "warnings",
        ],
    )

    return str(directions)


def remove_keys(obj, keys_to_remove):
    """
    Recursively remove all instances of any key in keys_to_remove from the dictionary or list obj.

    Args:
    obj (dict or list): The dictionary or list from which to remove the keys.
    keys_to_remove (list): A list of keys to be removed from the dictionary.

    Returns:
    dict or list: A new object with the specified keys removed.
    """
    if isinstance(obj, dict):
        return {
            key: remove_keys(value, keys_to_remove)
            for key, value in obj.items()
            if key not in keys_to_remove
        }
    elif isinstance(obj, list):
        return [remove_keys(item, keys_to_remove) for item in obj]
    else:
        return obj


mapping_tools = cast(
    List[BaseTool],
    [
        get_walking_directions,
        get_bicycling_directions,
        get_transit_directions,
    ],
)
