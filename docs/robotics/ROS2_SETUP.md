# ROS 2 Workspace Setup

## Distro and compatibility policy

ROS 2 Lyrical Luth is an LTS release, but the availability of ROS packages does not by itself establish compatibility of every robot stack. The ROS release documentation lists Lyrical as an LTS release supported until May 2031. PX4's current ROS 2 guide has recommended ROS 2 Jazzy on Ubuntu 24.04 as its supported/recommended platform. Therefore:

- Keep Lyrical as the requested development preference for the general ROS 2 workspace.
- Make PX4-on-Lyrical a compatibility spike and explicit release gate before committing to the UAV flight stack.
- If PX4 dependencies or simulator integration are not supported on Lyrical, evaluate a separate Jazzy/Ubuntu 24.04 development container or machine for the PX4 toolchain rather than mixing ROS distributions in one shell.
- Record tested ROS distro, Ubuntu version, PX4 tag, simulator version, middleware, and package versions in the compatibility matrix.

References: [ROS 2 Lyrical Luth release](https://github.com/ros2/ros2_documentation/blob/rolling/source/Releases/Release-Lyrical-Luth.rst) · [PX4 ROS 2 guide](https://docs.px4.io/main/en/ros/ros2_comm).

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
