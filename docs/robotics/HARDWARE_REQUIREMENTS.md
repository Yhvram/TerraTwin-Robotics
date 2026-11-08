# Hardware Requirements and Selection Criteria

This is a decision checklist, not a purchasing list. Select components only after interface and field constraints are known.

## UAV platform

| Subsystem | Required capability | Candidate direction |
|---|---|---|
| Airframe | Stable multirotor, payload margin, field maintainability | PX4-supported frame |
| Flight controller | PX4 support, safety inputs, GNSS/IMU interfaces | Pixhawk-class controller |
| Companion computer | ROS 2, camera pipeline, telemetry bridge | Jetson-class SBC or equivalent |
| Navigation | GNSS; RTK if required by mission tolerance | Supported GNSS receiver |
| Vision | Global-shutter/rolling-shutter choice based on motion and image task | RGB camera and calibrated mount |
| Communications | Independent operator link and companion telemetry link | RC plus radio/Wi-Fi/LTE as appropriate |
| Power | Verified current draw, flight-time margin, battery monitoring | Flight-rated battery and power module |

Before selecting: verify PX4 support, firmware target, companion interface, payload/flight-time budget, vibration isolation, GNSS placement, and legal operational requirements.

## UGV platform

| Subsystem | Required capability | Candidate direction |
|---|---|---|
| Chassis | Field clearance, traction, stability, serviceability | Differential drive or agreed steering geometry |
| Compute | ROS 2, Nav2, perception and logging headroom | Raspberry Pi 5 / Jetson-class computer |
| Motor control | Current/voltage margin, feedback, braking/safe stop | Industrial driver or suitable motor controller |
| Encoders | Resolution and interface matched to wheel/motor | Quadrature or integrated encoders |
| Localization | Wheel odometry + IMU + GNSS; optional LiDAR SLAM | Sensor suite matched to field geometry |
| Perception | Obstacle detection and crop-row sensing | LiDAR and/or RGB/depth camera |
| Power | Runtime, peak motor current, protected power rails | Battery, BMS, fusing and DC-DC converters |

Before selecting: verify ingress protection, dust/water resistance, thermal limits, vibration, wheel slip, traction, slope, turning radius, braking, emergency stop, and compute power budget.

## Shared acceptance checks

- Electrical interfaces and logic levels documented.
- Power budget calculated for peak and continuous load with safety margin.
- Connectors, strain relief, fuses, and emergency power isolation specified.
- Sensor field of view, mounting geometry, calibration, and frame IDs documented.
- Environmental ratings and operating-temperature range appropriate for agricultural use.
- Vendor support, ROS driver availability, ROS distro compatibility, and spare-part availability verified.
- Bench test procedure and replacement strategy documented.

## Purchase gate

Do not purchase a final platform BOM until the team has agreed mission requirements, target field size, soil/terrain, payload, expected runtime, required positional accuracy, connectivity assumptions, and budget.
