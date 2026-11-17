import time

import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node

from terratwin_interfaces.action import ExecuteMission
from terratwin_interfaces.msg import MissionResult


class MissionActionServer(Node):
    """Simulation-only Action server; it never commands physical actuators."""

    def __init__(self):
        super().__init__("terratwin_demo_mission_action_server")
        self.callback_group = ReentrantCallbackGroup()
        self.action_server = ActionServer(
            self,
            ExecuteMission,
            "/terratwin/execute_mission",
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            callback_group=self.callback_group,
        )
        self.get_logger().info("Simulation-only server ready")

    def goal_callback(self, goal_handle_request):
        request = goal_handle_request.request
        if not request.request_id or not request.mission_id or not request.waypoints:
            self.get_logger().warning("Rejecting mission: IDs and waypoints are required")
            return GoalResponse.REJECT
        if request.platform not in (request.UAV, request.UGV):
            self.get_logger().warning("Rejecting mission: platform must be UAV or UGV")
            return GoalResponse.REJECT
        if request.max_speed_mps < 0.0:
            self.get_logger().warning("Rejecting mission: max speed cannot be negative")
            return GoalResponse.REJECT

        expiry = request.expires_at
        expiry_ns = expiry.sec * 1_000_000_000 + expiry.nanosec
        if expiry_ns and expiry_ns <= self.get_clock().now().nanoseconds:
            self.get_logger().warning("Rejecting expired mission")
            return GoalResponse.REJECT

        return GoalResponse.ACCEPT

    def cancel_callback(self, _goal_handle):
        self.get_logger().info("Mission cancellation requested")
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        """Run a short simulation without relying on an asyncio event loop."""
        request = goal_handle.request.request
        terminal = MissionResult()
        terminal.request_id = request.request_id
        terminal.mission_id = request.mission_id

        for step in range(1, 6):
            if goal_handle.is_cancel_requested:
                terminal.status = MissionResult.CANCELED
                terminal.reason = "Canceled by Action client"
                terminal.completed_at = self.get_clock().now().to_msg()
                wrapped = ExecuteMission.Result()
                wrapped.result = terminal
                goal_handle.canceled()
                return wrapped

            # The reentrant callback group and multithreaded executor allow
            # cancellation callbacks to run while this simulation is waiting.
            time.sleep(0.5)

            feedback = ExecuteMission.Feedback()
            feedback.feedback.progress = step / 5.0
            feedback.feedback.current_waypoint_index = min(
                len(request.waypoints) - 1,
                int((step / 5.0) * len(request.waypoints)),
            )
            feedback.feedback.state = "SIMULATING"
            feedback.feedback.detail = "Demo only; no hardware is connected"
            feedback.feedback.current_pose_valid = False
            goal_handle.publish_feedback(feedback)

        terminal.status = MissionResult.SUCCEEDED
        terminal.reason = "Simulation completed; no physical robot was commanded"
        terminal.completed_at = self.get_clock().now().to_msg()
        wrapped = ExecuteMission.Result()
        wrapped.result = terminal
        goal_handle.succeed()
        return wrapped


def main(args=None):
    rclpy.init(args=args)
    node = MissionActionServer()
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
