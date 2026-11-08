# UAV Integration

## Goal

Integrate a PX4-compatible multirotor with ROS 2 for simulation, telemetry, supervised waypoint missions, image capture, and geotagging.

## Candidate stack

- PX4 flight controller and PX4 SITL.
- PX4 ROS 2 interfaces such as `px4_msgs` and `px4_ros_com`, plus the supported DDS transport/agent for the selected PX4 release.
- ROS 2 mission adapter and safety supervisor.
- GNSS, autopilot IMU, battery telemetry, and RGB camera.
- Gazebo Sim / PX4 simulation and RViz2 for visualization.

Treat this as a candidate integration, not a validated compatibility promise. Check PX4 release documentation against the selected ROS distro and simulator version before pinning versions.

## Stages

1. Run PX4 SITL and establish ROS 2 telemetry.
2. Verify timestamp, QoS, coordinate frame, and ENU/NED conversion behavior.
3. Publish/read vehicle status, local/global position, battery, and failsafe state.
4. Implement a ROS 2 Action for mission upload/execution with feedback and cancellation.
5. Add camera acquisition, calibration metadata, timestamps, and GNSS/pose association.
6. Implement and test geofence, stale-command rejection, low-battery policy, link-loss behavior, abort, and return-to-home.
7. Bench and field validate under an approved operating procedure with a human pilot/operator.

## Acceptance criteria

- SITL launch is reproducible from documented commands.
- Telemetry has documented units, frame conventions, timestamps, and QoS.
- Mission Action reports progress, terminal status, and meaningful failure reasons.
- Cancel/abort and PX4 failsafe transitions are verified in simulation.
- Camera frames can be associated with a valid pose and timestamp.
- No autonomous operation is enabled until safety tests and supervised flight approval are complete.

## Explicit v1 exclusion

No autonomous chemical spraying or payload release. Payload integration requires separate hazard analysis, authorization, operating procedures, and an independently reviewed safety case.
