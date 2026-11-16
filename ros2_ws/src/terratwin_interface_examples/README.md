# terratwin_interface_examples

Runnable ROS 2 examples for the TerraTwin interface package.

Build from ros2_ws:

    source /opt/ros/lyrical/setup.bash
    rosdep install --from-paths src --ignore-src -r -y
    colcon build --symlink-install --packages-up-to terratwin_interface_examples
    source install/setup.bash

Status publisher/subscriber (separate terminals):

    ros2 run terratwin_interface_examples status_subscriber
    ros2 run terratwin_interface_examples status_publisher

Mission Action server/client (separate terminals):

    ros2 run terratwin_interface_examples mission_action_server
    ros2 run terratwin_interface_examples mission_action_client

The client sends an expiring, one-waypoint UGV demo goal. The server emits five progress updates and returns a terminal result.

Safety: this is a software-only demonstration. It does not connect to motors, propellers, flight controllers or payloads. Simulated success is not authorization for physical motion.

Inspect the ROS graph:

    ros2 topic list
    ros2 topic echo /terratwin/robot_status
    ros2 action list
    ros2 action info /terratwin/execute_mission
