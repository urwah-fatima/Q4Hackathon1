---
sidebar_position: 3
title: "Chapter 1.3: Actions and Communication"
description: "Implement long-running robotic tasks with ROS 2 actions, featuring goals, feedback, and cancellation for humanoid motion control."
keywords: [ROS 2, actions, communication, feedback, goal, robotics]
---

# Chapter 1.3: Actions and Communication

**Prerequisites**: Chapter 1.2 (Nodes, Topics, and Services)
**Learning Objectives**: By the end of this chapter, you will be able to:
- Differentiate when to use actions versus services
- Implement action servers and clients for long-running tasks
- Handle goal feedback, cancellation, and preemption

## Concept Overview

Actions extend ROS 2's communication model for tasks that take significant time to complete and benefit from progress feedback. While services are synchronous and block the caller, actions are asynchronous—clients can monitor progress, cancel requests, and receive intermediate results. For humanoid robots, actions are essential for locomotion (walking to a goal), manipulation (grasping objects), and any task where real-time feedback enables adaptive behavior (Macenski et al., 2022).

## System Architecture

An action consists of three message types bundled together:

- **Goal**: The target state or command (e.g., "walk to position X,Y")
- **Feedback**: Periodic progress updates (e.g., "currently at position X',Y'")
- **Result**: Final outcome when the action completes (e.g., "reached goal" or "failed: obstacle")

The architecture involves:

- **Action Server**: Accepts goals, executes tasks, publishes feedback, returns results
- **Action Client**: Sends goals, receives feedback callbacks, can cancel active goals
- **State Machine**: Tracks goal states (pending, active, succeeded, canceled, aborted)

Under the hood, actions use a combination of services (for goal/cancel requests) and topics (for feedback/status), but the action API abstracts this complexity.

## Data Flow and Components

**Action Communication Sequence**:

1. Client sends goal via `send_goal()` service call
2. Server accepts/rejects goal based on current state
3. Server begins execution, publishes feedback on `/action_name/_action/feedback`
4. Client receives feedback through registered callback
5. On completion, server publishes result; client receives final status
6. Client may send cancel request at any time; server handles graceful termination

Action definitions (`.action` files) specify the Goal, Result, and Feedback message structures. The `action_msgs` package provides standard action types.

## Example Workflow

Action client sending a movement goal with feedback handling:

```python
# ROS 2 Humble | Python 3.10 | rclpy 3.3.x
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci  # Example action type

class MovementClient(Node):
    def __init__(self):
        super().__init__('movement_client')
        self._client = ActionClient(self, Fibonacci, 'move_humanoid')

    def send_goal(self, target):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = target

        self._client.wait_for_server()
        future = self._client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Progress: {feedback_msg.feedback.partial_sequence}')

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if goal_handle.accepted:
            self.get_logger().info('Goal accepted')
            goal_handle.get_result_async().add_done_callback(self.result_callback)

    def result_callback(self, future):
        self.get_logger().info(f'Result: {future.result().result.sequence}')
```

## Common Failure Modes

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| Goal rejection | Server refuses goal | Check server's goal policy; verify goal parameters |
| Feedback starvation | No progress updates | Ensure server publishes feedback; check topic connections |
| Cancellation ignored | Goal continues after cancel | Implement proper cancel handling in action server |
| Result timeout | Client waits indefinitely | Set timeouts; implement watchdog patterns |

## Summary

Actions provide the robust communication pattern needed for humanoid robot behaviors that unfold over time. The goal-feedback-result structure enables sophisticated task management including progress monitoring, cancellation, and error recovery. Most high-level humanoid behaviors—walking, manipulation, navigation—are implemented as actions.

**Next**: [Python Agents with rclpy](./rclpy-python-agents)

---

## References

1. Macenski, S., Foote, T., Gerkey, B., Lalancette, C., & Woodall, W. (2022). Robot Operating System 2: Design, architecture, and uses in the wild. *Science Robotics*, 7(66), eabm6074.

2. Open Robotics. (2023). *ROS 2 Humble documentation*. https://docs.ros.org/en/humble/
