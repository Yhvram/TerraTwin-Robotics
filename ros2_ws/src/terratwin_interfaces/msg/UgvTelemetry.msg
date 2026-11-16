# odometry frame_id and child_frame_id follow the documented TF convention.
std_msgs/Header header
string platform_id
nav_msgs/Odometry odometry
sensor_msgs/Imu imu
sensor_msgs/BatteryState battery
bool localization_valid
float32 linear_speed_mps
bool obstacle_stop_active
