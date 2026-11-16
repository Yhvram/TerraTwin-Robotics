# TerraTwin ROS 2 Interface Contract (Draft v0.1)

This is the first internal interface implementation for Issue #2. It is a draft, not a frozen external Brain API.

## Package boundaries

- terratwin_interfaces: domain messages and ExecuteMission Action.
- terratwin_interface_examples: simulation-only publisher/subscriber and Action client/server.
- Platform adapters publish UAV/UGV telemetry and translate platform-specific commands. The Brain bridge submits validated missions through the mission manager, never directly to actuator topics.

## Mission lifecycle

1. The bridge creates a MissionRequest with unique request_id, stable logical mission_id, target platform and platform ID, field, operation, timestamp, expiry and waypoints.
2. The mission manager validates schema, identity, expiry, coordinate frame/CRS, platform readiness and local safety permit.
3. The manager sends the request as the /terratwin/execute_mission Action goal.
4. The Action server publishes MissionFeedback, accepts cancellation and returns MissionResult.
5. The bridge correlates terminal results and telemetry using request and mission IDs.

The demo Action server simulates progress only. Production mission success must be based on platform-reported postconditions and independent safety checks.

## Interfaces

| Interface | ROS type | Intended use |
|---|---|---|
| /terratwin/robot_status | terratwin_interfaces/msg/RobotStatus | Readiness and health |
| UAV telemetry | terratwin_interfaces/msg/UavTelemetry | Pose, velocity, battery, flight mode and GPS validity |
| UGV telemetry | terratwin_interfaces/msg/UgvTelemetry | Odometry, IMU, battery, localization and obstacle stop |
| /terratwin/execute_mission | terratwin_interfaces/action/ExecuteMission | Long-running mission with feedback and cancellation |

Suggested platform telemetry topics are /uav/telemetry and /ugv/telemetry. Exact names, rates and QoS must be agreed before platform integration.

## Data conventions

- Timestamps use ROS time; sensor adapters should preserve acquisition timestamps where available.
- Cartesian positions and speeds are metres and metres/second. Geodetic latitude/longitude are degrees; altitude is metres and requires an agreed vertical datum.
- Cartesian waypoint frame_id identifies a ROS frame (for example map). Geodetic frame_id identifies its CRS (for example EPSG:4326).
- MissionRequest.header.stamp is request creation time. expires_at is an absolute ROS timestamp.
- request_id is unique per submission; mission_id remains stable across retries of the same logical mission. Receivers must enforce idempotency.
- UAV adapters must document PX4 NED/FRD to ROS ENU/FLU conversions. No implicit conversion is permitted.
- RobotStatus.battery_percentage is a fraction [0,1], or -1 when unknown.

## QoS and rates (initial guidance)

- Mission Action: use ROS Action protocol; enforce expiry and idempotency in application logic.
- Robot status: reliable, keep-last depth 10; target 1–2 Hz initially.
- Platform telemetry: sensor-data QoS for high-rate sensor streams; reliable QoS for discrete state transitions. Rates must be documented by each adapter.

## Review required before external freeze

- Brain/API maintainers must approve mission schema, authentication, authorization, field identifiers and CRS.
- Confirm operation enum, altitude datum, geofence representation and multi-waypoint policy.
- Confirm telemetry topic rates, QoS, retention and media URI semantics.
- Integrate an independent safety-supervisor permit before any hardware execution.
