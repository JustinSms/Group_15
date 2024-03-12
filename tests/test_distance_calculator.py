import sys
import pytest
from pathlib import Path

# Get the absolute path of the main_directory (parent of the current file's directory)
current_dir = Path(__file__).parent
main_directory_path = current_dir.parent / 'main_directory'

# Add the main_directory path to sys.path
sys.path.insert(0, str(main_directory_path))

# Now you can import haversine_distance
from distance_calculator import haversine_distance



def test_haversine_distance():
    # Define the coordinates of two points
    lat1, lon1 = 52.2296756, 21.0122287  # Warsaw
    lat2, lon2 = 41.8919300, 12.5113300  # Rome

    # Compute the distance between the two points
    distance = haversine_distance(lat1, lon1, lat2, lon2)

    # Check if the distance is correct
    assert round(distance,2) == pytest.approx(round(1447.6798872930887,2))


