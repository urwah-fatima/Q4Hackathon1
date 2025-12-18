---
sidebar_position: 2
title: "Nodes, Topics, and Services"
description: "Master ROS 2 communication primitives: nodes as computational units, topics for pub/sub messaging, and services for request/response patterns."
keywords: [ROS 2, nodes, topics, services, pub/sub, robotics]
---

# Nodes, Topics, and Services

**Prerequisites**: Chapter 1.1 (ROS 2 Architecture)
**Learning Objectives**: By the end of this chapter, you will be able to:
- Create and configure ROS 2 nodes
- Implement publish/subscribe communication using topics
- Build synchronous request/response patterns with services

## Concept Overview

Nodes, topics, and services form the core communication primitives in ROS 2. A **node** is a single-purpose process that performs computation—humanoid robots typically run dozens of nodes handling perception, planning, and control. **Topics** enable asynchronous publish/subscribe messaging for continuous data streams. **Services** provide synchronous request/response communication for discrete operations. Together, these primitives create the distributed computational graph that powers robotic systems (Quigley et al., 2009).

## System Architecture

The ROS 2 computational graph organizes nodes into a distributed system:

- **Nodes**: Independent processes with a single responsibility (e.g., camera driver, joint controller)
- **Publishers**: Nodes that send messages to named topics
- **Subscribers**: Nodes that receive messages from topics they've registered interest in
- **Service Servers**: Nodes that handle incoming requests and return responses
- **Service Clients**: Nodes that send requests and await responses

This separation enables modular development—each node can be developed, tested, and deployed independently. For humanoid robots, this means the vision processing node can be updated without affecting the locomotion controller, provided the interface contracts remain stable.

## Data Flow and Components

**Topic Communication Flow**:
1. Publisher creates a topic with a message type (e.g., `sensor_msgs/JointState`)
2. DDS announces the topic to the network
3. Subscribers discover and connect to matching topics
4. Messages flow asynchronously from publishers to all subscribers

**Service Communication Flow**:
1. Server advertises a service with request/response types
2. Client sends a request and blocks (or uses async callback)
3. Server processes request and returns response
4. Client receives response and continues execution

Standard message packages include `std_msgs` (primitives), `sensor_msgs` (sensors), and `geometry_msgs` (poses, transforms).

## Example Workflow

A publisher-subscriber pair demonstrating topic communication:

```python
# ROS 2 Humble | Python 3.10 | rclpy 3.3.x
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class JointPublisher(Node):
    def __init__(self):
        super().__init__('joint_publisher')
        self.publisher = self.create_publisher(Float64, 'joint_position', 10)
        self.timer = self.create_timer(0.1, self.publish_position)
        self.position = 0.0

    def publish_position(self):
        msg = Float64()
        msg.data = self.position
        self.publisher.publish(msg)
        self.position += 0.01

class JointSubscriber(Node):
    def __init__(self):
        super().__init__('joint_subscriber')
        self.subscription = self.create_subscription(
            Float64, 'joint_position', self.callback, 10)

    def callback(self, msg):
        self.get_logger().info(f'Received: {msg.data:.2f}')
```

## Common Failure Modes

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| Topic name mismatch | No messages received | Use `ros2 topic list` to verify exact names |
| Message type mismatch | Connection refused | Ensure publisher/subscriber use identical msg types |
| Service timeout | Client hangs indefinitely | Set explicit timeout; handle service unavailability |
| Queue overflow | Messages dropped | Increase queue depth or process messages faster |

## Summary

Nodes provide computational isolation, topics enable scalable data distribution, and services offer deterministic request/response patterns. These primitives form the communication backbone of any ROS 2 humanoid system. Mastering them is essential before exploring long-running tasks with actions.

**Next**: [Actions and Communication](./actions-communication)

---

## References

1. Quigley, M., Conley, K., Gerkey, B., Faust, J., Foote, T., Leibs, J., Wheeler, R., & Ng, A. Y. (2009). ROS: an open-source Robot Operating System. *ICRA Workshop on Open Source Software*, 3(3.2), 5.

2. Open Robotics. (2023). *ROS 2 Humble documentation*. https://docs.ros.org/en/humble/
