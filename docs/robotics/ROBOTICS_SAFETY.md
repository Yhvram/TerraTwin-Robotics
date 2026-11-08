# Robotics Safety Requirements

## Safety position

This document is a minimum engineering checklist, not a certification or substitute for local aviation, machinery, chemical, or workplace requirements. Each physical platform requires a platform-specific hazard analysis and approved operating procedure.

## Common safety supervisor

The safety supervisor must be able to veto mission start and request a safe stop/abort independently of the mission planner. Define explicit states such as DISARMED, READY, RUNNING, PAUSED, ABORTING, SAFE, and FAULT; document every valid transition.

Checks include:
- Hardware emergency stop and actuator-enable state.
- Operator authorization and mode.
- Geofence and mission bounds.
- Battery and critical hardware health.
- Sensor freshness and localization confidence.
- Communications heartbeat and command expiry.
- Maximum speed/altitude and permitted operating envelope.
- Obstacle state and platform failsafe status.

## UGV-specific controls

- Physical, accessible emergency stop that removes/halts drive torque according to the designed safe state.
- Speed limits and braking tests.
- Obstacle stop behavior and localization-loss response.
- Safe behavior on compute crash, motor-controller fault, or radio loss.
- Guarding and pinch-point assessment.

## UAV-specific controls

- Flight-controller arming checks and manufacturer/PX4 failsafes.
- Geofence, altitude, battery, RC/operator override, and link-loss configuration.
- Verified return-to-home/land/abort behavior for each test scenario.
- Propeller-safe test area and physical handling procedure.
- Human pilot/operator oversight and compliance with applicable aviation rules.

## Test matrix

| Fault injected | Expected response | Evidence |
|---|---|---|
| Mission expired | Reject before dispatch | Test result and log |
| Duplicate request | Idempotent response; no duplicate execution | Request/mission IDs |
| Heartbeat timeout | Platform-specific safe stop/failsafe | Bag and event log |
| Localization invalid | Pause or abort under defined policy | State and diagnostic record |
| Low battery | Reject, return, land, or stop per platform policy | Threshold and transition log |
| E-stop pressed | Hardware safe state; mission aborted | Physical test record |
| Sensor stale | Reject dependent behavior or enter safe mode | Diagnostic timestamp |
| Geofence violation predicted | Reject or prevent crossing | Simulated/bench test |

## Chemical payload / spraying exclusion

Autonomous chemical release is excluded from robotics v1. Before any future work, require chemical and environmental risk review, legal/operator approvals, application-rate control, physical interlocks, drift/overspray controls, emergency procedures, and a separately reviewed safety case. Do not test chemical release as part of navigation or perception development.
