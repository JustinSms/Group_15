"""Import the necessary libraries and download the datasets from the following links:"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import seaborn as sns
from shapely.geometry import LineString

# Download the datasets from the following links:
airlines_df = pd.read_csv("../downloads/airlines.csv")
airplanes_df = pd.read_csv("../downloads/airplanes.csv")
airports_df = pd.read_csv("../downloads/airports.csv")
routes_df = pd.read_csv("../downloads/routes.csv")

class FlightAnalyzer:
    def __init__(self, airlines_df, airplanes_df, airports_df, routes_df):
        self.airlines_df = airlines_df
        self.airplanes_df = airplanes_df
        self.airports_df = airports_df
        self.routes_df = routes_df
        self.world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    def method1(self, country_name: str):
        """
        Plot airports within a specified country on a map, focusing on the country.
        """
        self.airports_df['Latitude'] = pd.to_numeric(
            self.airports_df['Latitude'], errors='coerce')
        self.airports_df['Longitude'] = pd.to_numeric(
            self.airports_df['Longitude'], errors='coerce')
        self.airports_df = self.airports_df.dropna(subset=['Latitude', 'Longitude'])
        gdf_airports = gpd.GeoDataFrame(
            self.airports_df,
            geometry=gpd.points_from_xy(self.airports_df.Longitude,
                                        self.airports_df.Latitude))
        gdf_airports.crs = 'epsg:4326'
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        country = self.world[self.world.name == country_name]
        if country.empty:
            print(f"No country found with the name {country_name}.")
            # return (?)

        fig, ax = plt.subplots(figsize=(12, 10))
        world.plot(ax=ax, color='lightgrey')
        country.plot(ax=ax, color='whitesmoke', edgecolor='black')
        gdf_airports_within_country = gdf_airports[
            gdf_airports.geometry.within(country.geometry.unary_union)]
        gdf_airports_within_country.plot(
            ax=ax, marker='o', color='blue', markersize=5, alpha=0.6)
        minx, miny, maxx, maxy = country.total_bounds
        ax.set_xlim(minx, maxx)
        ax.set_ylim(miny, maxy)
        plt.title(f'Airports in {country_name}')
        ax.set_axis_off()
        plt.show()

    def method2(self):
        routes_df_2 = self.routes_df.copy()
        airports_df_2 = self.airports_df.copy()
        airports_df_2['Airport ID'] = pd.to_numeric(
            airports_df_2['Airport ID'], errors='coerce')
        routes_df_2['Source airport ID'] = pd.to_numeric(
            routes_df_2['Source airport ID'], errors='coerce')
        routes_df_2['Destination airport ID'] = pd.to_numeric(
            routes_df_2['Destination airport ID'], errors='coerce')
        airports_df_2.dropna(subset=['Airport ID'], inplace=True)
        routes_df_2.dropna(
            subset=['Source airport ID', 'Destination airport ID'], inplace=True)
        airports_df_2['Airport ID'] = airports_df_2['Airport ID'].astype(int)
        routes_df_2['Source airport ID'] = routes_df_2['Source airport ID'].astype(int)
        routes_df_2['Destination airport ID'] = routes_df_2['Destination airport ID'].astype(int)

        def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
            return geodesic((lat1, lon1), (lat2, lon2)).kilometers

        distances = []
        for index, route in routes_df_2.iterrows():
            source = airports_df_2[airports_df_2['Airport ID'] == route['Source airport ID']]
            destination = airports_df_2[
                airports_df_2['Airport ID'] == route['Destination airport ID']]
            if not source.empty and not destination.empty:
                print(f"Calculating distance between {source.iloc[0]['Name']} and {destination.iloc[0]['Name']}")
                source_lat = source.iloc[0]['Latitude']
                source_lon = source.iloc[0]['Longitude']
                dest_lat = destination.iloc[0]['Latitude']
                dest_lon = destination.iloc[0]['Longitude']
                print(f"Source: ({source_lat}, {source_lon}), Dest: ({dest_lat}, {dest_lon})")
                distance = calculate_distance(source_lat, source_lon, dest_lat, dest_lon)
                distances.append(distance)
                print(f"Distance: {distance} km")
            else:
                print(f"Missing airport data for route: {route}")

        if distances:
            plt.figure(figsize=(10, 6))
            sns.histplot(distances, bins=30, kde=True)
            plt.title('Distribution of Flight Distances')
            plt.xlabel('Distance (km)')
            plt.ylabel('Frequency')
            plt.show()
        else:
            print("No distances to plot.")


    def method3(self, airport: str, internal: bool = False):
        """
        Plot flight routes from a given airport using GeoPandas.
        If internal is True, plot only domestic flights.
        """
        source_country = self.airports_df[self.airports_df["IATA"] == airport]["Country"].iloc[0]

        # Filter routes by the specified source airport
        all_routes = self.routes_df[self.routes_df['Source airport'] == airport]

        # Filter for internal routes if specified
        if internal:
            all_routes = all_routes[
                all_routes['Destination airport'].isin(
                    self.airports_df[self.airports_df['Country'] == source_country]['IATA'])]

        # Merge routes with airport coordinates for plotting
        all_routes = all_routes.merge(
            self.airports_df[['IATA', 'Latitude', 'Longitude']],
            left_on='Source airport',
            right_on='IATA'
        )
        all_routes = all_routes.merge(
            self.airports_df[['IATA', 'Latitude', 'Longitude']],
            left_on='Destination airport',
            right_on='IATA',
            suffixes=('_source', '_dest')
        )

        # Create GeoDataFrame for routes
        all_routes['geometry'] = all_routes.apply(
            lambda x: LineString([
                (x['Longitude_source'], x['Latitude_source']),
                (x['Longitude_dest'], x['Latitude_dest'])
            ]), axis=1
        )
        geo_routes = gpd.GeoDataFrame(all_routes, geometry='geometry')
        geo_routes.crs = "EPSG:4326"

        # Setup for plotting
        fig, ax = plt.subplots(figsize=(15, 10))
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        world.plot(ax=ax, color='lightgrey')

        # Zoom in for internal flights
        country = world[world.name == source_country]
        if internal:
            minx, miny, maxx, maxy = country_geom.bounds
            ax.set_xlim(minx, maxx)
            ax.set_ylim(miny, maxy)
        country.plot(ax=ax, color='whitesmoke', edgecolor='black')

        # Plot the routes
        geo_routes.plot(ax=ax, color='blue', linewidth=0.5, alpha=0.5)

        plt.title(f"Flights from {airport} ({'Domestic' if internal else 'International'})")
        ax.set_axis_off()
        plt.show()

    def method4(self, N:int, country_input=None):
        """
        Develop a fourth method that may receive a string with a country or a list
        of country strings but has None by default. This method should plot the N
        most used airplane models by the number of routes. If the input argument is
        None, it should plot for the entire dataset. If it receives only a country
        or list of countries, it should plot just for that subset.
        """
        string_filter = isinstance(country_input, str)
        string_list_filter = isinstance(country_input, list) and all(
            isinstance(x, str) for x in country_input
        )

        try:
            assert string_filter == True    
        except:
            assert string_list_filter == True or country_input == None

        self.routes_df['Equipment'] = self.routes_df['Equipment'].astype(str)
        self.routes_df['Equipment'] = self.routes_df['Equipment'].dropna()

        if string_filter:
            country_input = [country_input]

        if country_input is None:
            country_input = self.airports_df['Country'].unique()

        equipment_list = []

        for country in country_input:
            target_country = self.airports_df[self.airports_df['Country'] == country]
            airports_target_country = target_country['IATA'].values

            routes_target_country = self.routes_df[
                self.routes_df['Source airport'].isin(airports_target_country)
            ]
            routes_target_country['Equipment'] = routes_target_country['Equipment'].str.split()
            exploded_df = routes_target_country.explode('Equipment')

            exploded_list = exploded_df['Equipment'].tolist()
            equipment_list += exploded_list

        equipment_series = pd.Series(equipment_list)
        equipment_df = equipment_series.value_counts().head(N).reset_index()
        equipment_df.columns = ['Equipment', 'Count']

        plt.figure(figsize=(10, 6))
        sns.barplot(data=equipment_df, x='Count', y='Equipment')
        plt.title(f'Top {N} Airplane Models by Number of Routes')
        plt.xlabel('Number of Routes')
        plt.ylabel('Airplane Model')
        plt.show()


    def method5_2(self, country_name: str, internal: bool=False, short_haul_cutoff=1000.0):
        """
        Plot internal and external flights for a specified country, 
        differentiating between short-haul and long-haul flights.
        Also, calculates the potential emission reduction 
        by replacing short-haul flights with rail services.

        Parameters:
        - country_name (str):
        The name of the country for which to plot flight routes.
        - internal (bool, optional):
        Whether to plot only internal flights. Defaults to False.
        - short_haul_cutoff (float, optional):
        The cutoff distance (in kilometers) to define short-haul flights. Defaults to 1000.
        """
        # Ensure necessary columns are present
        if not required_airports_cols.issubset(self.airports_df.columns):
            raise ValueError("Airports dataframe lacks required columns.")
        if not required_routes_cols.issubset(self.routes_df.columns):
            raise ValueError("Routes dataframe lacks required columns.")

        # Filter airports within the specified country
        country_airports = self.airports_df[self.airports_df['Country'] == country_name]
        if country_airports.empty:
            print(f"No airports found for the country: {country_name}")
            return

        # Filter routes for the specified country
        country_routes = self.routes_df[
            (self.routes_df['Source airport'].isin(country_airports['IATA'])) |
            (self.routes_df['Destination airport'].isin(country_airports['IATA']))
        ]

        # Further filter for internal flights if specified
        if internal:
            country_routes = country_routes[
                country_routes['Source airport'].isin(country_airports['IATA']) &
                country_routes['Destination airport'].isin(country_airports['IATA'])
            ]

        # Create LineStrings for routes
        routes_lines = country_routes.apply(
            lambda row: LineString([
                (self.airports_df.loc[self.airports_df['IATA'] == row['Source airport'],
                 'Longitude'].values[0], self.airports_df.loc[self.airports_df['IATA'] == row['Source airport'],
                 'Latitude'].values[0]),

                (self.airports_df.loc[self.airports_df['IATA'] == row['Destination airport'],
                'Longitude'].values[0], self.airports_df.loc[self.airports_df['IATA'] == row['Destination airport'],
                'Latitude'].values[0])
            ]), axis=1)
        routes_gdf = gpd.GeoDataFrame(country_routes, geometry=routes_lines)
        routes_gdf.crs = "EPSG:4326"

        # Calculate distances for each route
        routes_gdf['distance'] = routes_gdf.apply(lambda row: geodesic(
            (row.geometry.coords[0][1], row.geometry.coords[0][0]),
            (row.geometry.coords[1][1], row.geometry.coords[1][0])).kilometers, axis=1)
    
        # Distinguish routes based on cutoff distance
        short_haul = routes_gdf[routes_gdf['distance'] <= short_haul_cutoff]
        long_haul = routes_gdf[routes_gdf['distance'] > short_haul_cutoff]

        # Plotting setup
        fig, ax = plt.subplots(figsize=(15, 10))
        country = world[world.name == country_name]
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        world.plot(ax=ax, color='lightgrey')

        # Ensure the country plot is correctly drawn
        if not country.empty:
            country_to_plot = country[country.name == country_name]
            if not country_to_plot.empty:
                country_to_plot.plot(ax=ax, color='whitesmoke', edgecolor='black')
                if internal:
                    minx, miny, maxx, maxy = country_to_plot.total_bounds
                    ax.set_xlim(minx, maxx)
                    ax.set_ylim(miny, maxy)
        else:
            print(f"Could not find the country: {country_name} for plotting.")
            return

        # Plot long-haul flights first
        if not long_haul.empty:
            long_haul.plot(ax=ax, color='purple', linewidth=0.5, label='Long-haul flights')

        # Then plot short-haul flights
        if not short_haul.empty:
            short_haul.plot(ax=ax, color='orange', linewidth=0.5, label='Short-haul flights')

        # Annotations for number of routes and total distance of short-haul flights
        num_short_haul = len(short_haul)
        total_distance_short_haul = short_haul['distance'].sum()
        plt.annotate(f'Short-haul routes: {num_short_haul}\nTotal distance: {total_distance_short_haul:.2f} km', 
                    xy=(0.05, 0.95), xycoords='axes fraction', backgroundcolor='white')

        # Potential emission reduction calculation and annotation
        # Average CO2 emissions per passenger per kilometer for rail travel: 0.049 kg CO2 (Source: https://www.carbonindependent.org/21.html)
        # Average CO2 emissions per passenger per kilometer for air travel: 250 kg CO2 (Source: https://www.carbonindependent.org/22.html)

        # Parameters
        emissions_flight_per_km_per_passenger = 250
        emissions_rail_per_km_per_passenger = 0.049

        total_emissions_flight = total_distance_short_haul * emissions_flight_per_km_per_passenger
        total_emissions_rail = total_distance_short_haul * emissions_rail_per_km_per_passenger
        emission_reduction = total_emissions_flight - total_emissions_rail

        plt.annotate(f'Potential CO2 emission reduction by replacing short-haul flights with rail: {emission_reduction:.2f} kg',
             xy=(0.05, 0.9), xycoords='axes fraction', backgroundcolor='white')

        plt.legend()
        plt.title(f"{'Internal' if internal else 'All'} flights for {country_name} (Short-haul cutoff: {short_haul_cutoff} km)")
        ax.set_axis_off()
        plt.show()
