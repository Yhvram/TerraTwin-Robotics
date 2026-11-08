# TerraTwin Brain ↔ ROS 2 Integration

## Purpose

Define a safe boundary between the TerraTwin Brain/API and robot execution. The exact REST/MQTT contract must be agreed with the Brain maintainers before implementation.

## Direction

Brain -> bridge: mission proposal, field/plot identifier, target platform, waypoints or task parameters, deadline/expiry, request ID, schema version.

Bridge -> Brain: robot status, mission accepted/rejected, progress, completion/failure, telemetry references, fault and safety events.

## Contract requirements

Every request should carry:
- Unique request/mission ID and schema version.
- Creation time and expiry/deadline.
- Target platform and field/map reference.
- Explicit units and coordinate reference system.
- Requested operation and bounded parameters.
- Authorization/context needed to verify the sender.

Every response/event should carry:
- Original request ID and mission ID.
- Robot ID, platform, software version.
- Timestamp and sequence number.
- State, progress, terminal outcome, and machine-readable failure reason.
- Relevant telemetry or media references, not arbitrarily large inline payloads.

## Bridge behavior

- Authenticate and authorize inbound requests.
- Validate schema, freshness, platform availability, field bounds, and parameter limits.
- Reject duplicate requests or make them idempotent.
- Submit accepted work to the ROS 2 Mission Manager via an Action.
- Keep the local Safety Supervisor as the final execution gate.
- Bound retries and queues; use backoff for transient failures.
- Handle disconnect/reconnect and report uncertain outcomes explicitly.
- Never replay expired mission commands after reconnection.
- Do not allow Brain messages to command motors, propellers, or payloads directly.

## Open decisions

1. REST, MQTT, or hybrid transport and message broker ownership.
2. Authentication mechanism and device identity lifecycle.
3. Canonical field coordinate system and conversion service.
4. Telemetry retention, image storage, and signed URL strategy.
5. Mission state machine and error vocabulary.
6. Whether the Brain API already defines a mission schema that this bridge must adopt.

## Acceptance criteria

- Contract and sample payloads reviewed by Brain maintainers.
- Invalid, expired, duplicate, and unauthorized requests are rejected.
- Disconnect/reconnect tests do not execute stale commands.
- Mission status is correlated to the originating request.
