import rclpy
import time
from rclpy.node import Node
from geometry_msgs.msg import Twist
from roomba_sci.pyroombaadapter import PyRoombaAdapter

class RoombaSCINode(Node):
    def __init__(self):
        super().__init__('roomba_sci_node')

        # Initialize Roomba
        self.declare_parameter('serial_port', '/dev/serial0')
        serial_port = self.get_parameter('serial_port').value
        self.roomba = PyRoombaAdapter(serial_port)
        time.sleep(1)

        # Subscribers
        self.create_subscription(Twist, 'cmd_vel', self.cmd_vel_callback, 10)

        self.get_logger().info("Roomba ROS2 node started!")

    def cmd_vel_callback(self, msg:Twist):
        """Handle velocity commands"""
        self.get_logger().info(f'{msg.linear.x}_{msg.linear.y}')
        right_mm_sec = msg.linear.x
        left_mm_sec = msg.linear.y
        self.roomba.send_drive_direct(right_mm_sec, left_mm_sec)

    def destroy_node(self):
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = RoombaSCINode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down Roomba node...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
