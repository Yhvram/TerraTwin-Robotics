from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    xacro_file = PathJoinSubstitution(
        [FindPackageShare('terratwin_ugv'), 'urdf', 'terratwin_ugv.urdf.xacro'])
    rviz_config = PathJoinSubstitution(
        [FindPackageShare('terratwin_ugv'), 'config', 'ugv.rviz'])

    robot_description = ParameterValue(Command(['xacro ', xacro_file]), value_type=str)

    return LaunchDescription([
        DeclareLaunchArgument(
            'gui', default_value='true',
            description='Start joint_state_publisher_gui so wheels can be moved by hand.'),
        DeclareLaunchArgument(
            'rviz', default_value='true', description='Start RViz.'),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description,
                # Frames are published as ugv/base_link, ugv/lidar_link, ...
                'frame_prefix': 'ugv/',
                'use_sim_time': False,
            }],
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen',
            condition=IfCondition(LaunchConfiguration('gui')),
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config],
            output='screen',
            condition=IfCondition(LaunchConfiguration('rviz')),
        ),
    ])
