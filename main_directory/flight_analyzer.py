"""Import the necessary libraries and download the datasets from the following links:"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import seaborn as sns
from shapely.geometry import LineString

# Download the datasets from the following links:
airlines_df = pd.read_csv("downloads/airlines.csv")
airplanes_df = pd.read_csv("downloads/airplanes.csv")
airports_df = pd.read_csv("downloads/airports.csv")
routes_df = pd.read_csv("downloads/routes.csv")

class FlightAnalyzer:
    def __init__(self, airlines_df, airplanes_df, airports_df, routes_df):
        self.airlines_df = airlines_df
        self.airplanes_df = airplanes_df
        self.airports_df = airports_df
        self.routes_df = routes_df
        self.world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    def method1(self, country_name):
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
        country = self.world[self.world.name == country_name]
        if country.empty:
            print(f"No country found with the name {country_name}.")
            return
        fig, ax = plt.subplots(figsize=(12, 10))
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

        def calculate_distance(lat1, lon1, lat2, lon2):
            return geodesic((lat1, lon1), (lat2, lon2)).kilometers

        distances = []
        for index, route in routes_df_2.iterrows():
            source = airports_df_2[airports_df_2['Airport ID'] == route['Source airport ID']]
            destination = airports_df_2[
                airports_df_2['Airport ID'] == route['Destination airport ID']]
            if not source.empty and not destination.empty:
                source_lat = source.iloc[0]['Latitude']
                source_lon = source.iloc[0]['Longitude']
                dest_lat = destination.iloc[0]['Latitude']
                dest_lon = destination.iloc[0]['Longitude']
                distance = calculate_distance(source_lat, source_lon, dest_lat, dest_lon)
                distances.append(distance)

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
        """
        Plot flight routes from a given airport using GeoPandas.
        If internal is True, plot only domestic flights.
        """
        # Filter routes by the specified source airport
        all_routes = self.routes_df[self.routes_df['Source airport'] == airport]

        # Filter for internal routes if specified
        if internal:
            source_country = self.airports_df[
                self.airports_df["IATA"] == airport]["Country"].iloc[0]
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

        # Setup for plotting
        fig, ax = plt.subplots(figsize=(15, 10))
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

        # Zoom in for internal flights
        if internal:
            country_geom = world[world.name == source_country].geometry.unary_union
            minx, miny, maxx, maxy = country_geom.bounds
            ax.set_xlim(minx, maxx)
            ax.set_ylim(miny, maxy)
            world[world.name == source_country].plot(ax=ax, color='whitesmoke', edgecolor='black')
        else:
            world.plot(ax=ax, color='lightgrey')

        # Plot the routes
        geo_routes.plot(ax=ax, color='blue', linewidth=0.5, alpha=0.5)

        plt.title(f"Flights from {airport} ({'Domestic' if internal else 'International'})")
        ax.set_axis_off()
        plt.show()


    def method4(self, N, country_input=None):
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

        assert string_filter or string_list_filter or country_input is None

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


    def method5(self, country_name, internal=False):
        """
        Plot flight routes for a specified country. Optionally, filter for internal flights only.

        Parameters:
        - country_name (str): The name of the country for which to plot flight routes.
        - internal (bool, optional): Whether to plot only internal flights. Defaults to False.
        """
        # Ensure necessary columns are present
        required_airports_cols = {'IATA', 'Country', 'Latitude', 'Longitude'}
        required_routes_cols = {'Source airport', 'Destination airport'}
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

        # Plotting setup
        fig, ax = plt.subplots(figsize=(15, 10))
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        country = world[world.name == country_name]

        world.plot(ax=ax, color='lightgrey')

        # Adjust plot limits based on internal flag
        if internal:
            minx, miny, maxx, maxy = country.geometry.total_bounds
            ax.set_xlim(minx, maxx)
            ax.set_ylim(miny, maxy)
        else:
            ax.set_xlim(world.total_bounds[0], world.total_bounds[2])
            ax.set_ylim(world.total_bounds[1], world.total_bounds[3])

        country.plot(ax=ax, color='whitesmoke', edgecolor='black')
        routes_gdf.plot(ax=ax, color='blue', linewidth=0.5)

        plt.title(f"{'Internal' if internal else 'All'} flights for {country_name}")
        ax.set_axis_off()
        plt.show()
