---
sidebar_position: 4
title: "Chapter 1.4: Python Agents with rclpy"
description: "Build ROS 2 nodes in Python using rclpy, covering node lifecycle, executors, callbacks, and practical patterns for humanoid agents."
keywords: [ROS 2, rclpy, Python, agents, callbacks, robotics]
---

# Chapter 1.4: Python Agents with rclpy

**Prerequisites**: Chapter 1.3 (Actions and Communication)
**Learning Objectives**: By the end of this chapter, you will be able to:
- Create ROS 2 nodes using the rclpy Python client library
- Manage node lifecycle and configure executors
- Implement callbacks, timers, and parameter handling

## Concept Overview

rclpy (ROS Client Library for Python) is the official Python interface to ROS 2. It provides Pythonic APIs for creating nodes, publishers, subscribers, services, and actions. Python's accessibility makes rclpy ideal for rapid prototyping, AI/ML integration, and high-level behavior scripting in humanoid robots. While C++ (rclcpp) offers better real-time performance, rclpy excels for perception pipelines, planning algorithms, and integration with Python-based ML frameworks like PyTorch and TensorFlow (Open Robotics, 2023).

## System Architecture

rclpy follows a layered architecture:

- **Node Class**: Base class for all ROS 2 Python nodes; manages lifecycle, logging, and communication entities
- **Executors**: Process callbacks from subscriptions, timers, services, and actions
  - `SingleThreadedExecutor`: Sequential callback processing
  - `MultiThreadedExecutor`: Parallel callback processing via thread pool
- **Callback Groups**: Control callback concurrency (mutually exclusive or reentrant)
- **Context**: Global ROS 2 state; initialized with `rclpy.init()`, cleaned up with `rclpy.shutdown()`

For humanoid robots, the executor model is critical—perception callbacks must not block motor control callbacks. Proper use of executors and callback groups ensures responsive real-time behavior.

## Data Flow and Components

**Node Lifecycle**:
1. Initialize ROS context (`rclpy.init()`)
2. Create node instance (inherits from `Node`)
3. Create communication entities (publishers, subscribers, timers, services)
4. Spin node (executor processes callbacks)
5. Destroy node and shutdown context

**Key Components**:
- **Timers**: Periodic callback execution at specified frequency
- **Subscriptions**: Callbacks triggered on message arrival
- **Parameters**: Runtime-configurable values with type enforcement
- **Logging**: Severity-level logging with node name prefixing

## Example Workflow

A complete rclpy node demonstrating key patterns:

```python
# ROS 2 Humble | Python 3.10 | rclpy 3.3.x
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from std_msgs.msg import String

class HumanoidAgent(Node):
    def __init__(self):
        super().__init__('humanoid_agent')

        # Declare parameters with defaults
        self.declare_parameter('update_rate', 10.0)
        rate = self.get_parameter('update_rate').value

        # Create publisher
        self.status_pub = self.create_publisher(String, 'agent_status', 10)

        # Create timer for periodic updates
        self.timer = self.create_timer(1.0 / rate, self.update_callback)

        self.get_logger().info(f'Agent initialized at {rate} Hz')

    def update_callback(self):
        msg = String()
        msg.data = 'operational'
        self.status_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = HumanoidAgent()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Common Failure Modes

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| Callback blocking | System becomes unresponsive | Use async patterns; offload heavy computation |
| Executor starvation | Some callbacks never execute | Use MultiThreadedExecutor; review callback groups |
| Parameter type mismatch | Runtime errors on parameter access | Declare parameters with explicit types |
| Missing shutdown | Resource leaks, hanging processes | Use try/finally; implement signal handlers |

## Summary

rclpy provides the Python interface for building ROS 2 humanoid agents. Understanding executors and callback patterns is essential for building responsive systems. The combination of Python's ML ecosystem with ROS 2's robotics infrastructure makes rclpy the preferred choice for AI-driven humanoid behaviors.

**Next**: [URDF for Humanoid Modeling](./urdf-humanoid-modeling)

---

## References

1. Open Robotics. (2023). *ROS 2 Humble documentation*. https://docs.ros.org/en/humble/

2. Macenski, S., Foote, T., Gerkey, B., Lalancette, C., & Woodall, W. (2022). Robot Operating System 2: Design, architecture, and uses in the wild. *Science Robotics*, 7(66), eabm6074.
