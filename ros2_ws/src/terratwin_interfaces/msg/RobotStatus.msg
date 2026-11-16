# header.stamp is ROS time. battery_percentage is [0,1], or -1 if unknown.
uint8 PLATFORM_UNSPECIFIED=0
uint8 UAV=1
uint8 UGV=2
uint8 READINESS_UNSPECIFIED=0
uint8 NOT_READY=1
uint8 READY=2
uint8 BUSY=3
uint8 DEGRADED=4
uint8 FAULT=5
std_msgs/Header header
string platform_id
uint8 platform_type
uint8 readiness
bool emergency_stop_active
float32 battery_percentage
bool localization_valid
string[] active_faults
