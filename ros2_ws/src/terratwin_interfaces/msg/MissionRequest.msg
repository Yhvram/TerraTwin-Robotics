# header.stamp is request creation time in ROS time.
uint8 PLATFORM_UNSPECIFIED=0
uint8 UAV=1
uint8 UGV=2
std_msgs/Header header
string request_id
string mission_id
string platform_id
uint8 platform
string field_id
string operation
builtin_interfaces/Time expires_at
terratwin_interfaces/MissionWaypoint[] waypoints
float32 max_speed_mps
