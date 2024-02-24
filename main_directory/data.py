import pandas as pd
from math import radians, cos, sin, asin, sqrt

class AirlineDataAnalyzer:
    def __init__(self):
        # Load the datasets directly, without dropping any columns initially
        self.airlines_df = pd.read_csv('/mnt/data/airlines.csv')
        self.airplanes_df = pd.read_csv('/mnt/data/airplanes.csv')
        self.airports_df = pd.read_csv('/mnt/data/airports.csv')
        self.routes_df = pd.read_csv('/mnt/data/routes.csv')

        # Future steps might include cleaning specific columns or preparing data for merging
        # For now, all data is retained to preserve potential linking fields

    def calculate_distance(self, airport_id_1, airport_id_2):
        # Extract latitude and longitude for both airports
        airport_1 = self.airports_df[self.airports_df['Airport ID'] == airport_id_1]
        airport_2 = self.airports_df[self.airports_df['Airport ID'] == airport_id_2]
        
        if not airport_1.empty and not airport_2.empty:
            # Calculate distance using the Haversine formula
            lon1, lat1, lon2, lat2 = map(radians, [
                airport_1['Longitude'].values[0], 
                airport_1['Latitude'].values[0], 
                airport_2['Longitude'].values[0], 
                airport_2['Latitude'].values[0]
            ])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            r = 6371  # Radius of Earth in kilometers
            return c * r
        else:
            return None

# Example usage:
# analyzer = AirlineDataAnalyzer()
# distance = analyzer.calculate_distance(airport_id_1, airport_id_2)
# print(f"Distance: {distance} km")
