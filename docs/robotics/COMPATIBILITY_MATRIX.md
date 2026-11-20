# Compatibility Matrix (Issue #1)

Target for the UGV simulation stack: **ROS 2 Lyrical Luth on Ubuntu 26.04 (Resolute)** with **Gazebo Jetty**.

Status values: `Installable` = apt reports an installation candidate on the target OS (`scripts/check_lyrical_deps.sh`); `Verified` = built or run in this project's CI or container; `Unknown` = not yet checked.

Last apt check: 2026-11-20, Ubuntu 26.04 (resolute) in a VirtualBox VM, ROS apt source `ros2-apt-source`, command `ROS_DISTRO=lyrical bash scripts/check_lyrical_deps.sh`. All 14 packages had a candidate.

| Component | Role | Status | apt version (2026-11-20) | Notes |
|---|---|---|---|---|
| `ros-base` | Base distro | Verified | 0.13.0 | Workspace builds and passes tests, see log below |
| `ros2-control` | Control framework | Installable | 6.10.1 | |
| `ros2-controllers` | `diff_drive_controller` | Installable | 6.9.0 | `publish_rate` removed; use `tf_frame_prefix` |
| `gz-ros2-control` | Gazebo to ros2_control | Installable | 3.0.9 | Jetty only |
| `ros-gz` | Gazebo to ROS bridge | Installable | 3.0.10 | Pairs with Gazebo Jetty |
| `robot-localization` | EKF, `navsat_transform` | Installable | 3.10.0 | |
| `slam-toolbox` | Optional mapping | Installable | 2.10.0 | |
| `twist-mux` | Safety `cmd_vel` gate | Installable | 4.5.1 | |
| `navigation2` | Navigation | Installable | 1.5.2 | Earlier packaging issue (ros/rosdistro#53937) does not affect this apt source |
| `nav2-bringup` | Navigation launch | Installable | 1.5.2 | |
| `xacro` | Robot description | Installable | 2.1.1 | |
| `robot-state-publisher` | TF from URDF | Installable | 3.5.6 | |
| `joint-state-publisher` | Joint states | Installable | 2.4.3 | |
| `rviz2` | Visualization | Installable | 15.2.6 | |
| Gazebo Jetty | Simulator | Unknown | n/a | Pulled in by `ros-gz`; confirm `gz sim --version` after install |
| PX4 + ROS 2 | UAV | Out of scope | n/a | Separate spike (issue #7) |

Installable is not Verified. Only `ros-base` has been exercised so far; promote other rows to `Verified` as the simulation steps run them.

## Verification log

| Date | Environment | Command | Result |
|---|---|---|---|
| 2026-11-20 | Ubuntu 26.04 VM (VirtualBox), ROS 2 Lyrical, Python 3.14, pytest 9.0.2 | `colcon build --symlink-install && colcon test && colcon test-result --verbose` in `ros2_ws` | 8 packages built; 23 tests, 0 errors, 0 failures, 0 skipped |

Lyrical-specific notes from this run: the setuptools on Ubuntu 26.04 rejects `tests_require`, so Python packages declare test dependencies with `extras_require={'test': ['pytest']}`; `ament_flake8` enforces single quotes and `ament_copyright` requires a license header on Python files.

## Known Lyrical migration points

- `diff_drive_controller`: remove `publish_rate`; replace `tf_frame_prefix_enable` with `tf_frame_prefix` (for example `ugv`).
- `switch_controller` is strict by default; spawn/activate controllers in launch order.
- Use Gazebo Jetty SDF and `gz sim` commands.

## Running in a VM (VirtualBox)

3D acceleration is limited. Prefer headless simulation (`gz sim -s`) for tests, RViz for visualization, and LiDAR over camera sensors. Use the Docker image on a native host if rendering is too slow.

## Recording results

When a row is exercised, update its status to `Verified` and record: ROS distro, Ubuntu version, package version, Gazebo version, date, and the command that proved it.
