import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.duration import Duration
from terratwin_interfaces.action import ExecuteMission
from terratwin_interfaces.msg import MissionRequest, MissionWaypoint


class MissionActionClient(Node):
    def __init__(self):
        super().__init__("terratwin_demo_mission_action_client")
        self.client = ActionClient(self, ExecuteMission, "/terratwin/execute_mission")

    def send_demo_mission(self):
        self.get_logger().info("Waiting for mission Action server...")
        if not self.client.wait_for_server(timeout_sec=10.0):
            self.get_logger().error("Mission Action server not available")
            return False

        goal = ExecuteMission.Goal()
        request = MissionRequest()
        now = self.get_clock().now()
        request.header.stamp = now.to_msg()
        request.header.frame_id = "map"
        request.request_id = "demo-request-001"
        request.mission_id = "demo-mission-001"
        request.platform_id = "demo_ugv"
        request.platform = MissionRequest.UGV
        request.field_id = "demo-field"
        request.operation = "WAYPOINT_NAVIGATION"
        request.expires_at = (now + Duration(seconds=60)).to_msg()
        request.max_speed_mps = 0.25

        waypoint = MissionWaypoint()
        waypoint.coordinate_type = MissionWaypoint.CARTESIAN
        waypoint.frame_id = "map"
        waypoint.x_m = 1.0
        waypoint.y_m = 0.0
        waypoint.z_m = 0.0
        request.waypoints = [waypoint]
        goal.request = request

        send_future = self.client.send_goal_async(
            goal, feedback_callback=self.feedback_callback
        )
        rclpy.spin_until_future_complete(self, send_future)
        handle = send_future.result()
        if handle is None or not handle.accepted:
            self.get_logger().error("Mission goal rejected")
            return False

        result_future = handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        response = result_future.result()
        if response is None:
            self.get_logger().error("No terminal result received")
            return False
        mission_result = response.result.result
        self.get_logger().info(
            f"Mission status={mission_result.status}; reason={mission_result.reason}"
        )
        return mission_result.status == mission_result.SUCCEEDED

    def feedback_callback(self, message):
        feedback = message.feedback.feedback
        self.get_logger().info(
            f"Progress={feedback.progress:.0%}; state={feedback.state}; {feedback.detail}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = MissionActionClient()
    try:
        node.send_demo_mission()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
