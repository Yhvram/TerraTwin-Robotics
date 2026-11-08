# Contributing

## Workflow

1. Pick or create a GitHub issue describing the problem and measurable acceptance criteria.
2. Create a focused branch: `feature/<issue-number>-short-name` or `fix/<issue-number>-short-name`.
3. Keep changes small and buildable. Do not commit generated ROS build outputs.
4. Add unit, launch, integration, or reproducible manual tests appropriate to the change.
5. Update interface, units, frame, QoS, parameter, and safety documentation when behavior changes.
6. Open a pull request linking the issue and include test evidence and known limitations.

## ROS 2 conventions

- Prefer standard ROS messages when suitable; use custom interfaces only for domain-specific data.
- Use Actions for long-running missions, Services for short request/response operations, and Topics for streaming state.
- Explicitly document units, coordinate frames, timestamp source, QoS, and message version.
- Keep UAV and UGV namespaces/TF trees separate.
- Never send actuator commands directly from the Brain bridge; route missions through the mission manager and safety supervisor.

## Safety-critical changes

Changes affecting flight, drive, geofencing, failsafes, actuator enable, payloads, or emergency-stop behavior require a test plan and reviewer sign-off. Simulation-only success is not proof of physical safety.

## Scope

Autonomous chemical spraying is out of scope for robotics v1.
