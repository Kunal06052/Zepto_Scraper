import csv

# Delhi bounding box (approx)
min_lat, max_lat = 28.4042, 28.8832
min_lon, max_lon = 76.8376, 77.3636

# ~14m step in degrees latitude
lat_step = 0.000125

# For longitude, ~14m step at given latitude
import math
def lon_step(lat, step_meters=14):
    # 1 deg longitude in meters = 111320 * cos(lat)
    return step_meters / (111320 * math.cos(math.radians(lat)))

with open("delhi_grid_points.csv", "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["Latitude", "Longitude"])
    writer.writeheader()
    lat = min_lat
    while lat < max_lat:
        this_lon_step = lon_step(lat)
        lon = min_lon
        while lon < max_lon:
            writer.writerow({"Latitude": lat, "Longitude": lon})
            lon += this_lon_step
        lat += lat_step

print("Done! All grid points for Delhi written to delhi_grid_points.csv")
