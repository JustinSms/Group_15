"""Import the haversine_distance function from the distance_calculator module and test it"""
import sys
import os
import pytest

# Calculate the path to the functions directory and add it to sys.path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
functions_path = os.path.join(parent_dir, 'functions')
sys.path.insert(0, functions_path)

from distance_calculator import haversine_distance


def test_haversine_distance():
    """Test the haversine_distance function, by comparing the distance between two points"""
    # New York to New York
    assert haversine_distance(40.748817, -73.985428, 40.748817, -73.985428) == pytest.approx(
        0, rel=1e-4)
    # Berlin to Munich
    assert haversine_distance(52.5200, 13.4050, 48.1351, 11.5820) == pytest.approx(
        504.3, rel=1e-3)
    # Los Angeles to New York
    assert haversine_distance(34.0522, -118.2437, 40.7128, -74.0060) == pytest.approx(
        3933.1, rel=1e-3)
