# Robotics Task Backlog

The canonical task tracker is the GitHub Issues tab. This file provides the initial roadmap and links by issue title once created.

## Critical — foundation and safety

- [ ] Establish TerraTwin ROS 2 workspace, package conventions, namespaces, launch profiles, CI, and compatibility matrix.
- [ ] Define common ROS messages/actions for mission requests, robot status, faults, and telemetry.
- [ ] Implement an independent safety supervisor and fault-injection test plan.

## High — simulation and platform stacks

- [ ] Build an agricultural field simulation world with UAV and UGV models.
- [ ] Implement UGV robot description, sensor model, motor interface, encoder feedback, and odometry.
- [ ] Integrate UGV localization, mapping, obstacle handling, and Nav2 waypoint navigation.
- [ ] Establish PX4 SITL ↔ ROS 2 telemetry and coordinate-frame conversion.
- [ ] Implement a UAV mission Action with feedback, cancellation, and failsafe tests.
- [ ] Add camera acquisition, calibration metadata, timestamps, and geotagging.
- [ ] Agree the Brain API mission/status contract and implement the ROS 2 bridge.

## Medium — integration and prototype validation

- [ ] Validate end-to-end simulated missions for both platforms.
- [ ] Freeze hardware choices and perform bench bring-up.
- [ ] Conduct supervised field trials with documented safety sign-off.

## Explicitly not in v1

- [ ] Autonomous pesticide/herbicide spraying or chemical payload release. This needs separate policy approval, hazard analysis, legal/operator review, physical interlocks, and a dedicated safety case.
