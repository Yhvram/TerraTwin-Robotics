#!/usr/bin/env bash
# Checks that the APT packages needed by the UGV simulation stack are installable
# for the current ROS distro. Run inside the project container or an Ubuntu 26.04 host
# with the ROS apt source configured. Read-only: it installs nothing.
set -u

DISTRO="${ROS_DISTRO:-lyrical}"

PACKAGES=(
  ros-base
  ros2-control
  ros2-controllers
  gz-ros2-control
  ros-gz
  robot-localization
  slam-toolbox
  twist-mux
  navigation2
  nav2-bringup
  xacro
  robot-state-publisher
  joint-state-publisher
  joint-state-publisher-gui
  rviz2
)

missing=()
echo "Checking ros-${DISTRO}-* packages"
for pkg in "${PACKAGES[@]}"; do
  name="ros-${DISTRO}-${pkg}"
  candidate="$(apt-cache policy "$name" 2>/dev/null | awk '/Candidate:/ {print $2}')"
  if [ -z "$candidate" ] || [ "$candidate" = "(none)" ]; then
    printf '  MISSING  %s\n' "$name"
    missing+=("$name")
  else
    printf '  ok       %-45s %s\n' "$name" "$candidate"
  fi
done

if [ "${#missing[@]}" -gt 0 ]; then
  echo
  echo "Missing packages: ${missing[*]}"
  echo "Build them from source in ros2_ws/src or switch the affected component's plan; record the result in docs/robotics/COMPATIBILITY_MATRIX.md."
  exit 1
fi
echo "All checked packages have an installation candidate."
