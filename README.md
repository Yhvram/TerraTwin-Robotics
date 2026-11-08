# TerraTwin Robotics

ROS 2 robotics integration for TerraTwin: an autonomous agricultural UAV and a ground rover (UGV), connected to the TerraTwin Brain and digital-twin platform.

## Mission

Build and validate the robotics layer as a separate, reusable repository before proposing integration with the original [TerraTwin repository](https://github.com/ItsSriRamRahul/TerraTwin).

The first release focuses on reliable ROS 2 foundations, simulation, sensing, telemetry, waypoint navigation, and Brain API integration. Autonomous spot-treatment/spraying is **not** part of the initial release; it requires a separately reviewed mission policy, safety case, and operational procedures.

## Platforms

- **UAV:** PX4-compatible multirotor with ROS 2 offboard/mission integration, telemetry, camera capture, and geotagging.
- **UGV:** Differential-drive or other agreed rover base with motor control, encoders, IMU, GNSS, LiDAR/camera, localization, and Nav2 navigation.

Exact hardware is a design decision, not a fixed bill of materials. Confirm interfaces, environmental ratings, power budget, payload, and availability before purchasing.

## Technology direction

- ROS 2 Lyrical is the current development preference.
- PX4 + ROS 2 integration for the UAV; verify the PX4/ROS distro pairing separately before hardware selection.
- ROS 2 Control, Nav2, robot_localization, SLAM Toolbox for the UGV where appropriate.
- Gazebo Sim / ros_gz, RViz2, OpenCV and cv_bridge.
- A dedicated Brain bridge using documented APIs and/or MQTT; do not let the Brain bypass the onboard safety supervisor.

## Repository map

```text
docs/
  robotics/       Architecture and interface specifications
  plans/          Phased implementation plan
ros2_ws/src/
  terratwin_interfaces/
  terratwin_common/
  terratwin_mission_manager/
  terratwin_safety/
  terratwin_brain_bridge/
  terratwin_uav/
  terratwin_ugv/
  terratwin_simulation/
config/
launch/
maps/
models/
scripts/
tests/
```

Package directories are planned scaffolding targets; add packages incrementally with buildable commits and tests.

## Development principles

1. Simulate before connecting actuators.
2. Treat Brain requests as mission proposals; validate them locally before execution.
3. Use ROS 2 Actions for long-running missions so they support feedback, cancellation, and explicit results.
4. Keep safety supervision independent of mission-planning logic.
5. Log timestamped telemetry, mission transitions, safety interventions, and faults.
6. Use explicit units, coordinate frames, timestamps, and message versioning.
7. Never enable autonomous spraying based only on a successful navigation demo.

## Getting started

See [ROS 2 setup](docs/robotics/ROS2_SETUP.md), [architecture](docs/robotics/ROBOTICS_ARCHITECTURE.md), and the [implementation plan](docs/plans/robotics-v1.md).

## Scope boundary with TerraTwin Brain

The original TerraTwin project currently prioritizes irrigation scheduling. This repository owns robot-side integration and simulation. Spot-treatment remains a future integration point until the Brain-side policy, API contract, and safety requirements are explicitly approved.

## Contributing

Start with an issue from [TODO.md](TODO.md). Each change should include acceptance criteria, a test or reproducible validation procedure, and documentation for externally visible interfaces. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.
