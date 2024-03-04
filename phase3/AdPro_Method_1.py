import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Download the data
airports_df = pd.read_csv("downloads/airports.csv")

class FlightDataAnalysis:
    def __init__(self, airports_df):
        self.airports_df = airports_df
        self.world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    def plot_airports_by_country(self, country_name):
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

# Example usage:

# Initialize the class
flight_data_analyzer = FlightDataAnalysis(airports_df)

# Plot the airports for a specific country
flight_data_analyzer.plot_airports_by_country('United States of America')