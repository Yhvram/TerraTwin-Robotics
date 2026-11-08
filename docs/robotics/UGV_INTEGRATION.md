# UGV Integration

## Goal

Build a ROS 2 rover stack for agricultural field mapping, inspection, waypoint navigation, obstacle handling, and geotagged image acquisition.

## Candidate stack

- Differential-drive base (or documented alternative) with motor driver and wheel encoders.
- ROS 2 Control and `diff_drive_controller` where supported by the hardware.
- IMU, GNSS, LiDAR, RGB/depth camera as dictated by the prototype.
- `robot_localization` for sensor fusion.
- SLAM Toolbox for mapping where appropriate.
- Nav2 for global/local planning and navigation.
- URDF/Xacro robot description, RViz2 and Gazebo Sim.

Hardware selection is open. Validate motor-driver interfaces, encoder resolution, braking behavior, compute, sensor mounting, ingress protection, vibration, runtime, and power budget before ordering components.

## Stages

1. Create URDF/Xacro model, footprint, mass/inertial properties, and sensor frames.
2. Simulate drive kinematics and sensor topics in an agricultural field world.
3. Implement motor command interface, encoder feedback, and odometry.
4. Integrate IMU/GNSS and validate state estimation.
5. Add LiDAR/camera, map generation, and obstacle perception.
6. Bring up Nav2 with bounded speed, recovery behaviors, and geofenced goals.
7. Add waypoint mission Action and geotagged image capture.
8. Validate e-stop, communication loss, localization loss, stuck/blocked robot, and low-battery behavior.

## Acceptance criteria

- Robot model passes URDF checks and loads in RViz/Gazebo.
- Odometry is measured and compared with ground truth in simulation/bench tests.
- Frame tree is complete and free of duplicate TF publishers.
- Localization quality and failure states are observable.
- Nav2 handles a documented waypoint and obstacle scenario.
- Mission cancellation and safety stop halt commanded motion within the agreed test envelope.
