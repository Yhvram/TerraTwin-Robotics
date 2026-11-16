# Terminal mission outcome. completed_at uses ROS time.
uint8 STATUS_UNSPECIFIED=0
uint8 SUCCEEDED=1
uint8 REJECTED=2
uint8 FAILED=3
uint8 CANCELED=4
uint8 EXPIRED=5
string request_id
string mission_id
uint8 status
string reason
builtin_interfaces/Time completed_at
string telemetry_uri
