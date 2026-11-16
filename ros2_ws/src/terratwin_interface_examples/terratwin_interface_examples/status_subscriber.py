import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from terratwin_interfaces.msg import RobotStatus


class StatusSubscriber(Node):
    def __init__(self):
        super().__init__("terratwin_status_subscriber")
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.subscription = self.create_subscription(
            RobotStatus, "/terratwin/robot_status", self.status_callback, qos
        )
        self.get_logger().info("Listening on /terratwin/robot_status")

    def status_callback(self, msg):
        self.get_logger().info(
            f"platform={msg.platform_id} type={msg.platform_type} "
            f"readiness={msg.readiness} battery={msg.battery_percentage:.2f} "
            f"localization_valid={msg.localization_valid} "
            f"estop={msg.emergency_stop_active} faults={list(msg.active_faults)}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = StatusSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
