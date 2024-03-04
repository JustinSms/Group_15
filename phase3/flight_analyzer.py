import pandas as pd

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


    def method1(self):
        pass

    def method2(self):
        pass
           

    def method3(self, airport, internal=False):
        """Develop a third method that receives an airport as an input and an optional argument called internal 
        with a value of False by default. If internal is True, then this method should plot only the flights 
        leaving this airport with a destination in the same country. Otherwise, it plots all flights."""

        all_routes = routes_df[routes_df['Source airport'] == airport]

        if internal == False:
            print(all_routes)

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
            print("Tried the assert")      
        except:
            assert string_list_filter == True or country_input == None
            print("Tried the exepct assert")

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
            routes_target_country['Equipment'] = routes_target_country['Equipment'].str.split()
            exploded_df = routes_target_country.explode('Equipment')

            exploded_list = exploded_df["Equipment"].to_list()
            equipment_list += exploded_list

        equipment_series = pd.Series(equipment_list)
        print(equipment_series.value_counts().head(N))


        return equipment_series





        







    def method5(self, country_name, internal=False):
        """Develop a fifth method that receives a country name as an input and an optional argument called internal with a value of False by default.
        If internal is True, then this method should plot only the flights leaving the country with a destination in the same country.
        Otherwise, it plots all flights. This is analogous to the third method, but for country now."""
    # Filter the airports dataframe to get airports only in the given country
        country_airports = self.airports_df[self.airports_df['Country'] == country_name]['IATA'].unique()

        # Get all routes for the country
        country_routes = self.routes_df[
            (self.routes_df['Source airport'].isin(country_airports)) |
            (self.routes_df['Destination airport'].isin(country_airports))
        ]

        if internal:
            # Further filter for internal flights only
            country_routes = country_routes[
                (self.routes_df['Source airport'].isin(country_airports)) &
                (self.routes_df['Destination airport'].isin(country_airports))
            ]

        # Return the filtered routes
        return country_routes

FA = FlightAnalyzer(airlines_df, airplanes_df, airports_df, routes_df)
