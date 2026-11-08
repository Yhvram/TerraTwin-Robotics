# ROS 2 Workspace Setup

## Distro policy

Lyrical is the current working preference for development. Before declaring it the supported deployment distro, verify that the chosen Ubuntu release, ROS packages, PX4 ROS 2 bridge, Nav2, Gazebo integration, and third-party drivers are available and tested together. Record the exact OS image, ROS package versions, PX4 version, and simulator version in the project's compatibility matrix.

Do not mix ROS distributions in one shell or source multiple distro setup files into the same environment.

## Create the workspace

```bash
mkdir -p ~/terratwin_robotics_ws/src
cd ~/terratwin_robotics_ws
```

After packages have been added:

```bash
source /opt/ros/<ros_distro>/setup.bash
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

Replace `<ros_distro>` with the installed distro name. Run these commands in a clean shell.

## Useful validation

```bash
printenv | grep -E 'ROS_DISTRO|ROS_DOMAIN_ID|AMENT_PREFIX_PATH'
ros2 doctor --report
ros2 topic list
ros2 node list
colcon test
colcon test-result --verbose
```

## Workspace practices

- Keep source packages in `src/`; do not commit generated `build/`, `install/`, or `log/` directories.
- Pin tested dependency versions in documentation/CI; avoid assuming a driver supports the selected ROS distro.
- Use one `ROS_DOMAIN_ID` per isolated lab/test environment where discovery collisions are possible.
- Use namespaces and parameter files for platform separation.
- Put credentials and private endpoints in environment variables or a secrets manager, never in Git.
- Build and test in a clean environment before merging.

## Hardware bring-up order

1. Validate ROS graph and time synchronization without actuators.
2. Validate sensor drivers and frame IDs.
3. Validate state estimation against recorded data.
4. Validate motor/flight-controller integration with actuators disabled or safely restrained.
5. Test emergency stop and failsafes before any autonomous motion.
6. Progress from SITL/simulation to bench testing, then supervised field trials.
