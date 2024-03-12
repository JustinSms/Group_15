import sys
import pytest
from pathlib import Path

# Get the absolute path of the main_directory (parent of the current file's directory)
current_dir = Path(__file__).parent
main_directory_path = current_dir.parent / 'main_directory'

# Add the main_directory path to sys.path
sys.path.insert(0, str(main_directory_path))

# Now you can import haversine_distance
from flight_analyzer import FlightAnalyzer


def test_initialization(flight_analyzer):
    assert FlightAnalyzer.airlines_df is not None
    assert FlightAnalyzer.airplanes_df is not None
    assert FlightAnalyzer.airports_df is not None
    assert FlightAnalyzer.routes_df is not None

