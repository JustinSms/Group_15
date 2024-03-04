from geopy.distance import geodesic
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

airports_df = pd.read_csv("C:\\Users\\gilia\\OneDrive\\Dokumente\\Studium\\M.Sc. Business Analytics\\2nd Semester\\2612 - Advanced Programming for Data Science\\Group Project\\data\\airports.csv")
routes_df = pd.read_csv("C:\\Users\\gilia\\OneDrive\\Dokumente\\Studium\\M.Sc. Business Analytics\\2nd Semester\\2612 - Advanced Programming for Data Science\\Group Project\\data\\routes.csv")

# Define the calculate_distance function
def calculate_distance(lat1, lon1, lat2, lon2):
    # Calculate the great circle distance in kilometers between two points on the Earth
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers

# Define the FlightDataAnalysis class
class FlightDataAnalysis:
    def __init__(self, airports_df, routes_df):
        self.airports_df = airports_df
        self.routes_df = routes_df

    def distance_analysis(self):
        distances = []
        # Loop through each flight route
        for index, route in self.routes_df.iterrows():
            # Match the source and destination airports by ID
            source = self.airports_df[self.airports_df['Airport ID'] == route['Source airport ID']]
            destination = self.airports_df[self.airports_df['Airport ID'] == route['Destination airport ID']]
            if not source.empty and not destination.empty:
                # Print debug information
                print(f"Calculating distance between {source.iloc[0]['Name']} and {destination.iloc[0]['Name']}")
                source_lat = source.iloc[0]['Latitude']
                source_lon = source.iloc[0]['Longitude']
                dest_lat = destination.iloc[0]['Latitude']
                dest_lon = destination.iloc[0]['Longitude']
                print(f"Source: ({source_lat}, {source_lon}), Dest: ({dest_lat}, {dest_lon})")

                # Calculate the distance and append to the list
                distance = calculate_distance(source_lat, source_lon, dest_lat, dest_lon)
                distances.append(distance)
                print(f"Distance: {distance} km")  # This should not be zero or near-zero
            
            else:
                print(f"Missing airport data for route: {route}")
        
        # Plot the distribution of flight distances
        if distances:
            plt.figure(figsize=(10, 6))
            sns.histplot(distances, bins=30, kde=True)
            plt.title('Distribution of Flight Distances')
            plt.xlabel('Distance (km)')
            plt.ylabel('Frequency')
            plt.show()
        else:
            print("No distances to plot.")

# Initialize the FlightDataAnalysis class with your DataFrames
flight_data_analyzer = FlightDataAnalysis(airports_df, routes_df)

# Convert Airport IDs to integers for consistency
airports_df['Airport ID'] = pd.to_numeric(airports_df['Airport ID'], errors='coerce')
routes_df['Source airport ID'] = pd.to_numeric(routes_df['Source airport ID'], errors='coerce')
routes_df['Destination airport ID'] = pd.to_numeric(routes_df['Destination airport ID'], errors='coerce')

# Drop NaN values that resulted from coercion errors
airports_df.dropna(subset=['Airport ID'], inplace=True)
routes_df.dropna(subset=['Source airport ID', 'Destination airport ID'], inplace=True)

# Convert IDs to integer type if they are not already
airports_df['Airport ID'] = airports_df['Airport ID'].astype(int)
routes_df['Source airport ID'] = routes_df['Source airport ID'].astype(int)
routes_df['Destination airport ID'] = routes_df['Destination airport ID'].astype(int)

# Now run the distance_analysis method again
flight_data_analyzer.distance_analysis()