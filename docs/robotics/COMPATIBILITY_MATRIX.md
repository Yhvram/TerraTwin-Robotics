# Compatibility Matrix (Issue #1)

Target for the UGV simulation stack: **ROS 2 Lyrical Luth on Ubuntu 26.04 (Resolute)** with **Gazebo Jetty**.

Status values: `Verified` = built/run in this project's CI or container; `Released` = listed as released for Lyrical on the ROS package index but not yet exercised here; `Unknown` = must be checked with `scripts/check_lyrical_deps.sh`.

| Component | Role | Lyrical status | Notes |
|---|---|---|---|
| ROS 2 Lyrical Luth | Base distro | Released (LTS) | Ubuntu 26.04 |
| Gazebo Jetty | Simulator | Released | Pairs with Lyrical via `ros_gz` binaries |
| `ros_gz` | Gazebo <-> ROS bridge | Released (3.0.12) | Harmonic/Ionic are source-only on Lyrical |
| `gz_ros2_control` | Gazebo <-> ros2_control | Released (`lyrical` branch) | Jetty only |
| `ros2_control`, `ros2_controllers` | `diff_drive_controller` | Released (stable) | `publish_rate` removed; use `tf_frame_prefix` |
| `robot_localization` | EKF, `navsat_transform` | Released (4.0.0) | |
| `slam_toolbox` | Optional mapping | Released (2.10.0) | |
| `twist_mux` | Safety `cmd_vel` gate | Released (4.5.1) | |
| `navigation2`, `nav2_bringup` | Navigation | **Unknown** | Upstream 1.5.3 released, but an APT availability issue was reported for Ubuntu 26.04 (ros/rosdistro#53937). Run the check script; fall back to a source build if missing |
| PX4 + ROS 2 | UAV | Out of scope for this step | Separate compatibility spike (issue #7) |

Versions above come from the ROS package index and release announcements at the time of writing (2026-11-19) and must be re-verified by running the check script in the project container.

## Known Lyrical migration points

- `diff_drive_controller`: remove `publish_rate`; replace `tf_frame_prefix_enable` with `tf_frame_prefix` (for example `ugv`).
- `switch_controller` is strict by default; spawn/activate controllers in launch order.
- Use Gazebo Jetty SDF and `gz sim` commands.

## Running in a VM (VirtualBox)

3D acceleration is limited. Prefer headless simulation (`gz sim -s`) for tests, RViz for visualization, and LiDAR over camera sensors. Use the Docker image on a native host if rendering is too slow.

## Recording results

When a row is exercised, update its status to `Verified` and record: ROS distro, Ubuntu version, package version, Gazebo version, date, and the command that proved it.
