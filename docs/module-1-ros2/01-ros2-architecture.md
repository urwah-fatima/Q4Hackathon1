---
sidebar_position: 1
title: "ROS 2 Architecture"
description: "Learn the foundational architecture of ROS 2, including DDS middleware, QoS policies, and real-time capabilities for humanoid robotics."
keywords: [ROS 2, DDS, middleware, robotics, architecture, QoS]
---

# ROS 2 Architecture

**Prerequisites**: None
**Learning Objectives**: By the end of this chapter, you will be able to:
- Explain the role of DDS middleware in ROS 2
- Describe Quality of Service (QoS) policies and their applications
- Identify the key architectural improvements of ROS 2 over ROS 1

## Concept Overview

Robot Operating System 2 (ROS 2) is the next-generation robotics middleware framework designed for production-grade humanoid robots. Unlike its predecessor, ROS 2 uses the Data Distribution Service (DDS) as its communication layer, enabling real-time performance, enhanced security, and multi-platform support. For humanoid robotics, ROS 2 provides the essential infrastructure for coordinating complex perception-to-action pipelines across distributed computing nodes (Macenski et al., 2022).

## System Architecture

ROS 2's architecture centers on DDS, an industry-standard middleware that handles message serialization, discovery, and transport. The key architectural components include:

- **DDS Layer**: Manages peer-to-peer discovery and data distribution without a central master node
- **ROS Middleware Interface (rmw)**: Abstracts DDS implementations, allowing vendor flexibility
- **ROS Client Libraries (rcl)**: Provides language bindings (rclpy, rclcpp) for node development
- **Quality of Service (QoS)**: Configurable policies for reliability, durability, deadline, and history

This layered design enables humanoid robots to maintain real-time control loops while simultaneously processing high-bandwidth sensor data. QoS policies allow developers to tune communication characteristics—using reliable delivery for critical joint commands while accepting best-effort for camera streams (Open Robotics, 2023).

## Data Flow and Components

In ROS 2, data flows through a computational graph consisting of nodes, topics, services, and actions:

1. **Discovery**: Nodes announce themselves via DDS multicast; no central rosmaster required
2. **Topics**: Asynchronous publish/subscribe channels for streaming data (sensor readings, commands)
3. **Services**: Synchronous request/response for discrete operations
4. **Actions**: Long-running tasks with feedback (walking, manipulation)

Messages are defined in `.msg` files and compiled into language-specific types. The graph structure supports dynamic reconfiguration—nodes can join or leave without system restart, critical for humanoid robots operating in unpredictable environments.

## Example Workflow

Below is a minimal ROS 2 node demonstrating the architecture:

```python
# ROS 2 Humble | Python 3.10 | rclpy 3.3.x
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy

class MinimalNode(Node):
    def __init__(self):
        super().__init__('architecture_demo')

        # Configure QoS for reliable delivery
        qos = QoSProfile(depth=10)
        qos.reliability = ReliabilityPolicy.RELIABLE

        self.get_logger().info('Node initialized with DDS middleware')

def main():
    rclpy.init()
    node = MinimalNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

This example initializes a node with explicit QoS configuration, demonstrating how ROS 2 exposes DDS capabilities directly to application code.

## Common Failure Modes

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| DDS discovery failure | Nodes cannot find each other | Check `ROS_DOMAIN_ID` matches across all nodes |
| QoS incompatibility | Publisher/subscriber not connecting | Ensure compatible QoS profiles (reliable-to-reliable) |
| Network multicast blocked | Discovery works locally only | Configure DDS for unicast or check firewall settings |

## Summary

ROS 2's DDS-based architecture provides the foundation for building robust humanoid robot systems. The middleware layer handles discovery, serialization, and transport, while QoS policies enable fine-grained control over communication characteristics. Understanding this architecture is essential before working with ROS 2's communication primitives.

**Next**: [Nodes, Topics, and Services](./nodes-topics-services)

---

## References

1. Macenski, S., Foote, T., Gerkey, B., Lalancette, C., & Woodall, W. (2022). Robot Operating System 2: Design, architecture, and uses in the wild. *Science Robotics*, 7(66), eabm6074.

2. Open Robotics. (2023). *ROS 2 Humble documentation*. https://docs.ros.org/en/humble/
