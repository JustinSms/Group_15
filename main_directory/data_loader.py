import os
import requests
import zipfile
import pandas as pd

class AirlineDataAnalyzer:
    def __init__(self):
        print("Initializing AirlineDataAnalyzer...")
        self.downloads_dir = './downloads'
        self.zip_url = 'https://gitlab.com/adpro1/adpro2024/-/raw/main/Files/flight_data.zip?inline=false'
        self.ensure_downloads_dir_exists()
        self.download_and_extract_zip()

    def ensure_downloads_dir_exists(self):
        """Ensure the downloads directory exists within the project."""
        try:
            if not os.path.exists(self.downloads_dir):
                os.makedirs(self.downloads_dir)
                print(f"Created directory: {self.downloads_dir}")
            else:
                print(f"Directory already exists: {self.downloads_dir}")
        except Exception as e:
            print(f"Error ensuring downloads directory exists: {e}")

    def download_and_extract_zip(self):
        """Download the ZIP file and extract its contents."""
        zip_path = os.path.join(self.downloads_dir, 'flight_data.zip')
        
        try:
            # Download ZIP file if it doesn't already exist
            if not os.path.exists(zip_path):
                print("Downloading ZIP file...")
                response = requests.get(self.zip_url)
                with open(zip_path, 'wb') as zip_file:
                    zip_file.write(response.content)
                print("Downloaded ZIP file.")
            else:
                print("ZIP file already exists. Skipping download.")

            # Extract the ZIP file
            print("Extracting ZIP file...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.downloads_dir)
            print("Extracted ZIP file.")
        except Exception as e:
            print(f"Error downloading or extracting ZIP file: {e}")
        
        self.load_data_files()

    def load_data_files(self):
        """Load the extracted CSV files into pandas DataFrames."""
        try:
            self.airlines_df = pd.read_csv(os.path.join(self.downloads_dir, 'airlines.csv'))
            self.airplanes_df = pd.read_csv(os.path.join(self.downloads_dir, 'airplanes.csv'))
            self.airports_df = pd.read_csv(os.path.join(self.downloads_dir, 'airports.csv')).drop(columns=['Type', 'Source'], errors='ignore')
            self.routes_df = pd.read_csv(os.path.join(self.downloads_dir, 'routes.csv'))
            print("Data loaded successfully into DataFrames.")
        except Exception as e:
            print(f"Error loading data files into DataFrames: {e}")

# Example of how to run the class
if __name__ == '__main__':
    analyzer = AirlineDataAnalyzer()

print(analyzer.airlines_df.head())
print(analyzer.airplanes_df.head())
print(analyzer.airports_df.head())
print(analyzer.routes_df.head())