# Cartesian x/y/z: metres in frame_id. Geodetic lat/lon: degrees; altitude: metres.
# For geodetic coordinates frame_id identifies the CRS (for example EPSG:4326).
uint8 CARTESIAN=0
uint8 GEODETIC=1
uint8 coordinate_type
string frame_id
float64 x_m
float64 y_m
float64 z_m
float64 latitude_deg
float64 longitude_deg
float64 altitude_m
