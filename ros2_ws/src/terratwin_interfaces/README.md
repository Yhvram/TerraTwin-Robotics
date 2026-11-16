# terratwin_interfaces

Common ROS 2 interfaces for TerraTwin UAV and UGV applications.

Messages:
- MissionWaypoint: Cartesian metres or geodetic degrees/metres, with explicit frame/CRS.
- MissionRequest: request and mission IDs, platform, field, operation, expiry and waypoints.
- MissionResult: terminal state, reason, completion time and optional telemetry URI.
- MissionFeedback: progress, waypoint index, execution state and optional current pose.
- RobotStatus: readiness, E-stop state, battery fraction, localization validity and faults.
- UavTelemetry: pose, velocity, battery, armed state, flight mode and GPS/altitude validity.
- UgvTelemetry: odometry, IMU, battery, localization, speed and obstacle-stop state.

Action:
- ExecuteMission: request goal, terminal result, periodic feedback and cancellation.

Build from ros2_ws:
    source /opt/ros/lyrical/setup.bash
    rosdep install --from-paths src --ignore-src -r -y
    colcon build --symlink-install --packages-up-to terratwin_interfaces
    source install/setup.bash

Inspect:
    ros2 interface show terratwin_interfaces/msg/RobotStatus
    ros2 interface show terratwin_interfaces/action/ExecuteMission

Conventions: ROS timestamps; Cartesian positions in metres; speed in m/s; latitude/longitude in degrees; altitude in metres. request_id identifies an attempt; mission_id remains stable across retries. Cartesian frame_id identifies a ROS frame; geodetic frame_id identifies a CRS. PX4 NED-to-ROS ENU conversion must be explicit in the UAV adapter. Battery fraction is [0,1], or -1 when unknown.

This is an initial internal contract. Brain/API owners must review it before external API freeze.
