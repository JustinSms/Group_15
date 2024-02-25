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

    def method2(self, airport, internal=False):
        """Develop a third method that receives an airport as an input and an optional argument called internal 
        with a value of False by default. If internal is True, then this method should plot only the flights 
        leaving this airport with a destination in the same country. Otherwise, it plots all flights."""

        if internal == False:
            all_routes = self.routes_df[self.routes_df['Source airport'] == airport]
            print(all_routes)

        if internal == True:
            internal
            
            #print(internal_routes)
           

    def method3(self):
        pass

    def method4(self):
        pass    

    def method5(self): 
        pass



FA = FlightAnalyzer(airlines_df, airplanes_df, airports_df, routes_df)
FA.method2('MUC')