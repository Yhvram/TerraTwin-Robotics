# Sensor and ROS Interface Specification

## Common rules

- Use standard ROS messages where they fit; create custom interfaces only for domain-specific fields.
- Document topic name, type, publisher, rate, QoS, units, frame_id, timestamp source, and calibration.
- Use SI units unless the interface explicitly states otherwise.
- Use ROS time consistently and identify whether timestamps are sensor, host, or synchronized time.
- Include covariance when the sensor or estimator can provide it.
- Never rely on topic names alone to infer coordinate conventions.

## Suggested topics

| Platform | Topic | Suggested type | Notes |
|---|---|---|---|
| UAV | `/uav/pose` | `geometry_msgs/PoseWithCovarianceStamped` | Define local frame and ENU/NED conversion |
| UAV | `/uav/battery` | `sensor_msgs/BatteryState` | Voltage, percentage, health when known |
| UAV | `/uav/camera/image_raw` | `sensor_msgs/Image` | Pair with CameraInfo |
| UGV | `/ugv/odom` | `nav_msgs/Odometry` | Define odom/base frames |
| UGV | `/ugv/imu` | `sensor_msgs/Imu` | Calibrated axes and covariance |
| UGV | `/ugv/scan` | `sensor_msgs/LaserScan` | Laser frame and scan limits |
| UGV | `/ugv/fix` | `sensor_msgs/NavSatFix` | Datum and covariance status |
| Common | `/terratwin/robot_status` | custom status | Readiness and fault state |
| Common | `/diagnostics` | `diagnostic_msgs/DiagnosticArray` | Component health |

## QoS

Select QoS deliberately for each stream. Sensor streams often use sensor-data QoS; mission commands and state transitions need reliable delivery and explicit expiry/idempotency at the application layer. Record durability, reliability, history, and depth in the interface table.

## Calibration and geotagging

Store camera intrinsics/distortion, sensor extrinsics, calibration date, device identity, and calibration version. Geotag records should include source image timestamp, pose timestamp, coordinate reference system, position covariance/quality, and the transform/calibration versions used.
