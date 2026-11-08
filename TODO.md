# Robotics Task Backlog

The detailed acceptance criteria and discussion live in GitHub Issues.

## P0 — foundation and safety

- [ ] [#1 Establish ROS 2 workspace and compatibility matrix](https://github.com/Yhvram/TerraTwin-Robotics/issues/1)
- [ ] [#2 Define common ROS 2 mission, status and telemetry interfaces](https://github.com/Yhvram/TerraTwin-Robotics/issues/2)
- [ ] [#10 Implement independent robotics safety supervisor](https://github.com/Yhvram/TerraTwin-Robotics/issues/10)

## P1 — simulation and platform stacks

- [ ] [#3 Build agricultural field simulation world for UAV and UGV](https://github.com/Yhvram/TerraTwin-Robotics/issues/3)
- [ ] [#4 Create UGV URDF/Xacro and sensor model](https://github.com/Yhvram/TerraTwin-Robotics/issues/4)
- [ ] [#5 Implement UGV motor control, encoder feedback and odometry](https://github.com/Yhvram/TerraTwin-Robotics/issues/5)
- [ ] [#6 Integrate UGV localization, SLAM and Nav2 navigation](https://github.com/Yhvram/TerraTwin-Robotics/issues/6)
- [ ] [#7 Validate PX4 SITL and ROS 2 telemetry bridge](https://github.com/Yhvram/TerraTwin-Robotics/issues/7)
- [ ] [#8 Implement UAV waypoint mission Action and failsafe handling](https://github.com/Yhvram/TerraTwin-Robotics/issues/8)
- [ ] [#9 Add crop image acquisition, calibration and geotagging](https://github.com/Yhvram/TerraTwin-Robotics/issues/9)
- [ ] [#11 Implement TerraTwin Brain API ↔ ROS 2 bridge](https://github.com/Yhvram/TerraTwin-Robotics/issues/11)

## P2 — integration and prototype validation

- [ ] [#12 Validate end-to-end UAV and UGV missions in simulation](https://github.com/Yhvram/TerraTwin-Robotics/issues/12)
- [ ] [#13 Freeze prototype hardware and perform supervised field validation](https://github.com/Yhvram/TerraTwin-Robotics/issues/13)

## Explicitly not in v1

Autonomous pesticide/herbicide spraying or chemical payload release is excluded. It requires separate policy approval, hazard analysis, legal/operator review, physical interlocks, and a dedicated safety case.
