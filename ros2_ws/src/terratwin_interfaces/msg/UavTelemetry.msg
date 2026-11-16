# UAV adapter must document PX4 NED/FRD to ROS ENU/FLU conversion.
std_msgs/Header header
string platform_id
geometry_msgs/PoseWithCovarianceStamped pose
geometry_msgs/TwistStamped velocity
sensor_msgs/BatteryState battery
bool armed
string flight_mode
bool gps_valid
float32 relative_altitude_m
bool relative_altitude_valid
