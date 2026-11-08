# TerraTwin Robotics Architecture

## 1. System context

```text
TerraTwin Brain / Digital Twin
        |  mission proposal, field context, telemetry
        v
Brain API / MQTT Gateway
        |
        v
ROS 2 Mission Manager
        |
        +---- Safety Supervisor (independent veto / stop path)
        |
        +---- UAV adapter ---- PX4 flight controller ---- UAV
        |
        +---- UGV adapter ---- motor controllers ---------- Rover
        |
        +---- Perception, localization, diagnostics, logging
```

The Brain plans and evaluates farm operations. ROS 2 owns device integration, state estimation, mission execution, and local safety enforcement. The safety supervisor may reject, pause, or abort commands regardless of the source.

## 2. Main ROS 2 packages

| Package | Responsibility |
|---|---|
| `terratwin_interfaces` | Versioned messages, services, and actions shared across platforms |
| `terratwin_common` | Parameters, frame conventions, diagnostics helpers, lifecycle utilities |
| `terratwin_mission_manager` | Validate and sequence platform-independent missions |
| `terratwin_safety` | Geofence, health gates, timeout handling, emergency-stop coordination |
| `terratwin_brain_bridge` | Authenticated API/MQTT exchange and schema mapping |
| `terratwin_uav` | PX4 adapter, UAV sensors, mission execution, camera/geotagging |
| `terratwin_ugv` | Robot description, base control, localization, Nav2, sensors |
| `terratwin_simulation` | Field world, platform models, sensor and mission scenarios |

Keep platform-specific message adapters at the boundary. Do not couple core mission logic to a particular flight controller or motor driver.

## 3. Namespace and frame conventions

Use namespaces `/uav` and `/ugv`. Each platform must have its own TF tree. Recommended frame names:

- Common: `map`, `earth` (only where geodetic integration is used).
- UGV: `ugv/odom`, `ugv/base_link`, `ugv/base_footprint`, sensor frames.
- UAV: `uav/map` or a documented local navigation frame, `uav/base_link`, camera and autopilot frames.

Do not publish competing TF authorities for the same transform. Document ENU/NED conversions at the PX4 boundary. Geodetic coordinates, local Cartesian coordinates, and ROS frame coordinates are different representations and must never be silently mixed.

## 4. Interface direction

Suggested topic families (final names and schemas must be agreed with the Brain/API team):

| Interface | Type | Direction / purpose |
|---|---|---|
| `/uav/pose` | PoseWithCovarianceStamped or approved custom state | UAV state |
| `/uav/battery` | BatteryState | UAV power |
| `/uav/camera/image_raw` | Image | Camera frames |
| `/ugv/odom` | Odometry | Rover odometry |
| `/ugv/scan` | LaserScan | LiDAR |
| `/ugv/imu` | Imu | Inertial data |
| `/terratwin/robot_status` | custom status | Health and readiness |
| `/terratwin/telemetry` | custom telemetry or mapped standard messages | Telemetry |
| `/terratwin/mission` | Mission action interface | Mission request/execution |

Use Actions for long-running missions (feedback, cancellation, terminal result). Use Services for short request/response operations. Use Topics for continuous state/telemetry. Avoid using a single unbounded string or loosely structured JSON topic as the internal ROS contract.

## 5. Mission execution lifecycle

1. Receive a mission proposal from a trusted Brain endpoint.
2. Validate schema, platform, map/field boundary, waypoint limits, freshness, and robot readiness.
3. Ask the safety supervisor for an execution permit.
4. Dispatch a ROS 2 Action to the selected platform adapter.
5. Publish progress and health; accept cancellation and pause/abort requests.
6. Report terminal result, failure reason, and relevant telemetry.
7. Persist a mission event record for audit and debugging.

A mission is not considered complete merely because the final waypoint was sent; require platform-reported completion and verify postconditions.

## 6. Safety architecture

The safety supervisor must independently check, as applicable:

- Emergency-stop state and actuator enable state.
- Geofence / permitted operating area.
- Battery and critical subsystem health.
- Localization validity and sensor freshness.
- Communication heartbeat and command age.
- Speed, altitude, and motion constraints.
- Mission authorization and operating mode.
- Obstacle state and platform-specific failsafe state.

Define deterministic behavior for every failed check: reject before start, pause, controlled stop, land/return-to-home, or operator handoff as appropriate. A ROS node alone is not a substitute for hardware-level emergency stop or flight-controller failsafes.

## 7. Brain integration boundary

The bridge translates authenticated Brain-side mission and telemetry contracts into ROS interfaces. It must implement request IDs, schema/version checks, timeouts, retries with idempotency, bounded queues, and explicit error states. The Brain must not publish directly to low-level actuator topics.

## 8. Deployment and observability

Provide launch profiles for simulation, bench testing, and field operation. Include ROS diagnostics, structured logs, rosbag recording profiles, parameter snapshots, software version information, and a documented recovery procedure.

## 9. Non-goals for robotics v1

- Autonomous pesticide/herbicide spraying.
- Unsupervised operation around people, animals, roads, or public areas.
- Claims of production-grade agricultural autonomy before field validation.
- A single shared TF tree for UAV and UGV.
