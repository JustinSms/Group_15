import sys
import pytest
import pandas as pd
from pathlib import Path


current_directory = Path(__file__).resolve().parent
# Go up two levels to the parent directory of main_directory
project_directory = current_directory.parent.parent
sys.path.append(str(project_directory))

from main_directory.flight_analyzer import FlightAnalyzer

airlines_df = pd.read_csv("../downloads/airlines.csv")
airplanes_df = pd.read_csv("../downloads/airplanes.csv")
airports_df = pd.read_csv("../downloads/airports.csv")
routes_df = pd.read_csv("../downloads/routes.csv")

FA = FlightAnalyzer(airlines_df=airlines_df, airports_df=airports_df, routes_df=routes_df, airplanes_df=airplanes_df)