import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import seaborn as sns
from shapely.geometry import LineString

# Download the data
airlines_df = pd.read_csv("downloads/airlines.csv")
airplanes_df = pd.read_csv("downloads/airplanes.csv")
airports_df = pd.read_csv("downloads/airports.csv")
routes_df = pd.read_csv("downloads/routes.csv")

class FlightAnalyzer():

    def __init__ (self, airlines_df, airplanes_df, airports_df, routes_df):
        self.airlines_df = airlines_df
        self.airplanes_df = airplanes_df
        self.airports_df = airports_df
        self.routes_df = routes_df
        self.world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    def method1(self, country_name):
        
        # Ensure the DataFrame has the right data types
        self.airports_df['Latitude'] = pd.to_numeric(self.airports_df['Latitude'], errors='coerce')
        self.airports_df['Longitude'] = pd.to_numeric(self.airports_df['Longitude'], errors='coerce')

        # Drop any rows with NaN values in Latitude or Longitude
        self.airports_df = self.airports_df.dropna(subset=['Latitude', 'Longitude'])

        # Convert the DataFrame to a GeoDataFrame
        gdf_airports = gpd.GeoDataFrame(
            self.airports_df,
            geometry=gpd.points_from_xy(self.airports_df.Longitude, self.airports_df.Latitude)
        )
        gdf_airports.crs = {'init': 'epsg:4326'}

        # Filter the world GeoDataFrame for the country of interest
        country = self.world[self.world.name == country_name]

        # If the country is not found, return
        if country.empty:
            print(f"No country found with the name {country_name}.")
            return

        # Create a base plot
        fig, ax = plt.subplots(figsize=(10, 15))

        # Plot the country
        country.plot(ax=ax, color='white', edgecolor='black')

        # Plot the airports on top, within the country's boundaries
        gdf_airports_within_country = gdf_airports[gdf_airports.geometry.within(country.geometry.squeeze())]
        gdf_airports_within_country.plot(ax=ax, color='blue', markersize=10)

        # Final touches
        plt.title(f'Airports in {country_name}')
        ax.set_axis_off()  # Optional: Turns off the axis
        plt.show()
        pass

    def method2(self):
        
        routes_df_2 = self.routes_df.copy()
        airports_df_2 = self.airports_df.copy()

        # Convert Airport IDs to integers for consistency
        airports_df_2['Airport ID'] = pd.to_numeric(airports_df_2['Airport ID'], errors='coerce')
        routes_df_2['Source airport ID'] = pd.to_numeric(routes_df_2['Source airport ID'], errors='coerce')
        routes_df_2['Destination airport ID'] = pd.to_numeric(routes_df_2['Destination airport ID'], errors='coerce')

        # Drop NaN values that resulted from coercion errors
        airports_df_2.dropna(subset=['Airport ID'], inplace=True)
        routes_df_2.dropna(subset=['Source airport ID', 'Destination airport ID'], inplace=True)

        # Convert IDs to integer type if they are not already
        airports_df_2['Airport ID'] = airports_df_2['Airport ID'].astype(int)
        routes_df_2['Source airport ID'] = routes_df_2['Source airport ID'].astype(int)
        routes_df_2['Destination airport ID'] = routes_df_2['Destination airport ID'].astype(int)

        # Define the calculate_distance function
        def calculate_distance(lat1, lon1, lat2, lon2):
            # Calculate the great circle distance in kilometers between two points on the Earth
            return geodesic((lat1, lon1), (lat2, lon2)).kilometers
        
        distances = []

        # Loop through each flight route
        for index, route in routes_df_2.iterrows():
            # Match the source and destination airports by ID
            source = airports_df_2[airports_df_2['Airport ID'] == route['Source airport ID']]
            destination = airports_df_2[airports_df_2['Airport ID'] == route['Destination airport ID']]
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

    def method3(self, airport, internal=False):
        """Develop a third method that receives an airport as an input and an optional argument called internal 
        with a value of False by default. If internal is True, then this method should plot only the flights 
        leaving this airport with a destination in the same country. Otherwise, it plots all flights."""

        all_routes = routes_df[routes_df['Source airport'] == airport]

        if internal == False:
            print(all_routes)

            return all_routes

        if internal == True:
        
            source_country = airports_df[airports_df["IATA"] == airport]["Country"].values[0]

            airports_source_country = airports_df[airports_df["Country"] == source_country]["IATA"].values

            destination_source_country = all_routes[all_routes["Destination airport"].isin(airports_source_country)]

            print(destination_source_country)

            return destination_source_country

    def method4(self, N: int, country_input = None):
        """Develop a fourth method that may receive a string with a country or a list of country strings 
        but has None by default. This method should plot the N most used airplane models by number of routes. 
        If the input argument is None it should plot for all dataset. If it receives only a country or list of 
        countries, it should plot just for that subset."""  

        string_filter = isinstance(country_input, str)
        string_list_filter = isinstance(country_input, list) and all(isinstance(x, str) for x in country_input)

        try:
            assert string_filter == True    
        except:
            assert string_list_filter == True or country_input == None

        routes_df["Equipment"] = routes_df["Equipment"].astype(str)
        routes_df["Equipment"] = routes_df["Equipment"].dropna()

        if string_filter == True:
            country_input = [country_input]

        if country_input == None:
            country_input = airports_df["Country"].unique()

        equipment_list = []

        for country in country_input:

            target_country = airports_df[airports_df["Country"] == country]
            airports_target_country = target_country["IATA"].values

            routes_target_country = routes_df[routes_df["Source airport"].isin(airports_target_country)]
            routes_target_country.loc[:, 'Equipment'] = routes_target_country['Equipment'].str.split()
            exploded_df = routes_target_country.explode('Equipment')

            exploded_list = exploded_df["Equipment"].to_list()
            equipment_list += exploded_list

        equipment_series = pd.Series(equipment_list)
        print(equipment_series.value_counts().head(N))

        return equipment_series

    def method5(self, country_name, internal=False):
        """
        Plot flight routes for a specified country. Optionally, filter for internal flights only.
        Parameters:
        - country_name (str): The name of the country for which to plot flight routes.
        - internal (bool, optional): Whether to plot only internal flights. Defaults to False.
        """
        # Ensure airports and routes dataframes are prepared with necessary columns
        if not set(['IATA', 'Country', 'Latitude', 'Longitude']).issubset(self.airports_df.columns):
            raise ValueError("Airports dataframe lacks required columns.")
        if not set(['Source airport', 'Destination airport']).issubset(self.routes_df.columns):
            raise ValueError("Routes dataframe lacks required columns.")
    
        # Filter airports within the specified country
        country_airports = self.airports_df[self.airports_df['Country'] == country_name]
        if country_airports.empty:
            print(f"No airports found for the country: {country_name}")
            return

        # Filter routes starting from or ending in the country's airports
        country_routes = self.routes_df[(self.routes_df['Source airport'].isin(country_airports['IATA'])) | 
                                        (self.routes_df['Destination airport'].isin(country_airports['IATA']))]
    
        # If internal is True, further filter for routes where both source and destination are within the country
        if internal:
            country_routes = country_routes[country_routes['Source airport'].isin(country_airports['IATA']) & 
                                            country_routes['Destination airport'].isin(country_airports['IATA'])]

        # Create LineStrings for routes
        routes_lines = country_routes.apply(lambda row: LineString([
            (self.airports_df.loc[self.airports_df['IATA'] == row['Source airport'], 'Longitude'].values[0], 
             self.airports_df.loc[self.airports_df['IATA'] == row['Source airport'], 'Latitude'].values[0]),
            (self.airports_df.loc[self.airports_df['IATA'] == row['Destination airport'], 'Longitude'].values[0], 
             self.airports_df.loc[self.airports_df['IATA'] == row['Destination airport'], 'Latitude'].values[0])
        ]), axis=1)
        routes_gdf = gpd.GeoDataFrame(country_routes, geometry=routes_lines)
        routes_gdf.crs = "EPSG:4326"

        # Plotting
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        country = world[world.name == country_name]
    
        fig, ax = plt.subplots(figsize=(12, 8))
        world.plot(ax=ax, color='lightgrey')
    
        # Focus on the country of interest by setting plot limits
        if internal:
            # When plotting internal flights, zoom in to the country's extent
            minx, miny, maxx, maxy = country.geometry.total_bounds
            ax.set_xlim(minx, maxx)
            ax.set_ylim(miny, maxy)
        else:
            # Otherwise, show the world map for context
            ax.set_xlim(world.total_bounds[0], world.total_bounds[2])
            ax.set_ylim(world.total_bounds[1], world.total_bounds[3])
    
        country.plot(ax=ax, color='whitesmoke', edgecolor='black')
        routes_gdf.plot(ax=ax, color='blue', linewidth=0.5)

        plt.title(f"{'Internal' if internal else 'All'} flights for {country_name}")
        ax.set_axis_off()
        plt.show()
