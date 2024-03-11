import numpy as np
import unittest

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance in kilometers between two points
    on the Earth specified by their latitude and longitude in decimal degrees.
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    # Radius of Earth in kilometers (KM)
    r = 6371.0
    return c * r

class TestHaversineDistance(unittest.TestCase):
    def test_distance(self):
        # Test case 1: Within the same city
        self.assertAlmostEqual(haversine_distance(48.8566, 2.3522, 48.864716, 2.349014), 0.9, places=1)

        # Test case 2: Between two cities
        self.assertAlmostEqual(haversine_distance(52.5200, 13.4050, 48.8566, 2.3522), 878, delta=1)

        # Test case 3: Between two continents
        self.assertAlmostEqual(haversine_distance(34.0522, -118.2437, 48.8566, 2.3522), 9085, delta=1)

if __name__ == '__main__':
    unittest.main()
