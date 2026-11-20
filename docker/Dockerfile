# Development image for the TerraTwin robotics workspace.
# Base image tag is an assumption: confirm that an official ROS image for the target
# distro exists (docker pull ros:${ROS_DISTRO}-ros-base) and adjust ROS_DISTRO if needed.
ARG ROS_DISTRO=lyrical
FROM ros:${ROS_DISTRO}-ros-base

ARG ROS_DISTRO
ENV ROS_DISTRO=${ROS_DISTRO} \
    DEBIAN_FRONTEND=noninteractive

# Packages that are expected to exist for the UGV simulation stack.
# If one is missing for this distro, scripts/check_lyrical_deps.sh reports it;
# do not silently drop it here.
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      git \
      python3-colcon-common-extensions \
      python3-pytest \
      python3-rosdep \
      ros-${ROS_DISTRO}-ros2-control \
      ros-${ROS_DISTRO}-ros2-controllers \
      ros-${ROS_DISTRO}-robot-localization \
      ros-${ROS_DISTRO}-twist-mux \
      ros-${ROS_DISTRO}-xacro \
      ros-${ROS_DISTRO}-robot-state-publisher \
      ros-${ROS_DISTRO}-ros-gz \
      ros-${ROS_DISTRO}-gz-ros2-control \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY scripts/check_lyrical_deps.sh /usr/local/bin/check_lyrical_deps.sh
RUN chmod +x /usr/local/bin/check_lyrical_deps.sh

SHELL ["/bin/bash", "-c"]
CMD ["bash"]
