import json

import numpy

from ..generators.random_road_generator import RandomRoadGenerator
from ..generators.segmented_road_generator import SegmentedRoadGenerator

def coords_to_json(
    x: numpy.ndarray,
    y: numpy.ndarray,
    filename: str = "output.json",
    x_key: str = "x",
    y_key: str = "y"
) -> str:
    """Convert x and y arrays of waypoints to a JSON.

    Args:
        x (numpy.ndarray): x coordinates.
        y (numpy.ndarray): y coordinates.
        x_key (str, optional): Key for x coordinates. Defaults to "x".
        y_key (str, optional): Key for y coordinates. Defaults to "y".

    Returns:
        str: JSON string containing the data.
    """
    data = {
        x_key: x.tolist(),  # Convert numpy array to list
        y_key: y.tolist()
    }

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
        
def params_to_json(
    generator: RandomRoadGenerator | SegmentedRoadGenerator,
    filename: str = "output.json"
):

    params = {}
    
    for attr in dir(generator):
        # skip private and special attributes
        if not attr.startswith('_'):
            value = getattr(generator, attr)
            if not callable(value):
                params[attr] = value

    with open(filename, "w") as file:
        json.dump(params, file, indent=4)