cmake_minimum_required(VERSION 3.8)
project(terratwin_interfaces)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/MissionWaypoint.msg"
  "msg/MissionRequest.msg"
  "msg/MissionResult.msg"
  "msg/MissionFeedback.msg"
  "msg/RobotStatus.msg"
  "msg/UavTelemetry.msg"
  "msg/UgvTelemetry.msg"
  "action/ExecuteMission.action"
  DEPENDENCIES builtin_interfaces geometry_msgs nav_msgs sensor_msgs std_msgs
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(test_interface_contract test/test_interface_contract.py)
endif()

ament_export_dependencies(rosidl_default_runtime)
ament_package()
