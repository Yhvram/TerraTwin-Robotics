# Robotics v1 Implementation Plan

## Objective

Deliver a tested ROS 2 software foundation for a simulated and then supervised physical UAV and UGV, with a well-defined TerraTwin Brain integration boundary.

## Scope

**In scope:** ROS 2 workspace and interfaces, simulation, sensor integration, UGV navigation, UAV PX4 SITL/telemetry/waypoint workflows, image geotagging, safety supervision, Brain bridge, prototype validation.

**Out of scope:** autonomous spraying/chemical release, unsupervised public-area operation, production-readiness claims without field evidence.

## Work phases and exit gates

### P0 — Architecture and ROS 2 foundation
- Decide distro/OS/CI compatibility matrix.
- Create package skeletons, namespaces, interface conventions, TF policy, diagnostics and logging.
- Define mission/status interfaces with Brain team.
- Exit: clean workspace builds; interface and frame documentation reviewed.

### P1 — Simulation
- Create a simple agricultural field world.
- Add UAV and UGV models and sensor streams.
- Build repeatable launch scenarios and rosbag capture.
- Exit: both models launch, publish expected topics, and run repeatable scenario tests.

### P2 — UGV autonomy
- Base control, encoders, odometry and IMU/GNSS fusion.
- LiDAR/camera integration, mapping and Nav2.
- Waypoint mission Action, obstacle handling and stop behavior.
- Exit: repeatable simulated navigation and safe-stop test; then bench tests with wheels raised/drive disabled as appropriate.

### P3 — UAV autonomy foundation
- PX4 SITL and ROS 2 bridge.
- Vehicle telemetry and coordinate conversion.
- Waypoint mission Action, camera capture and geotagging.
- Exit: SITL mission, cancellation, link-loss and failsafe scenarios pass.

### P4 — Brain integration
- Implement contract-approved REST/MQTT bridge.
- Validate, authorize, dispatch, track and report mission lifecycle.
- Test duplicate, expired, malformed and disconnected cases.
- Exit: end-to-end simulated mission request and telemetry round trip.

### P5 — Physical prototypes and supervised trials
- Freeze hardware bill of materials and operating procedures.
- Calibrate sensors and validate e-stop/failsafes.
- Begin controlled, supervised, low-risk trials.
- Exit: documented test evidence and approval to expand operating envelope.

## Indicative sequencing

| Workstream | Relative window |
|---|---|
| P0 foundation | Weeks 1–2 |
| P1 simulation | Weeks 3–4 |
| P2 UGV | Weeks 5–7 |
| P3 UAV | Weeks 6–8 |
| P4 Brain bridge | Weeks 9–10 |
| P5 prototype/field validation | Week 11 onward |

This is a planning estimate, not a delivery commitment; hardware lead times, compatibility, and safety review can change the sequence.

## Initial milestones

1. **M1 — ROS 2 foundation:** workspace, interfaces, frames, CI and coding conventions.
2. **M2 — Simulation:** UAV/UGV models and agricultural field test world.
3. **M3 — UGV navigation:** control, localization, Nav2, safety tests.
4. **M4 — UAV integration:** PX4 SITL, mission Action, camera/geotagging.
5. **M5 — Brain integration:** approved API bridge and end-to-end simulation.
6. **M6 — Prototype validation:** hardware bring-up, e-stop and supervised trials.

## Definition of done

A feature is done when it builds in the documented environment, has relevant automated or reproducible tests, documents units/frames/QoS/parameters, reports diagnostics and failure modes, and has no unresolved safety-critical issue. Physical autonomy requires its own test sign-off.
