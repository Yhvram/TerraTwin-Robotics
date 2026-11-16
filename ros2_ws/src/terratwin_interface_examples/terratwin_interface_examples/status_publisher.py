import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from terratwin_interfaces.msg import RobotStatus


class StatusPublisher(Node):
    def __init__(self):
        super().__init__("terratwin_status_publisher")
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.publisher = self.create_publisher(RobotStatus, "/terratwin/robot_status", qos)
        self.timer = self.create_timer(1.0, self.publish_status)
        self.sequence = 0
        self.get_logger().info("Publishing demo UGV status")

    def publish_status(self):
        msg = RobotStatus()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "ugv/base_link"
        msg.platform_id = "demo_ugv"
        msg.platform_type = RobotStatus.UGV
        msg.readiness = RobotStatus.READY
        msg.emergency_stop_active = False
        msg.battery_percentage = 0.85
        msg.localization_valid = True
        msg.active_faults = []
        self.publisher.publish(msg)
        self.sequence += 1
        self.get_logger().info(
            f"Published status #{self.sequence}: {msg.platform_id}, "
            f"readiness={msg.readiness}, battery={msg.battery_percentage:.0%}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = StatusPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
