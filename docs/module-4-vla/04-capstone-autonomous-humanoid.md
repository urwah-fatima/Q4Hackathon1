---
sidebar_position: 4
title: "Capstone: Autonomous Humanoid"
description: "Integrate all modules into a complete autonomous humanoid system capable of voice-commanded manipulation and navigation."
keywords: [capstone, integration, autonomous, humanoid, end-to-end, Physical AI]
---

# Capstone: Autonomous Humanoid

**Prerequisites**: Chapters 4.1-4.3 (VLA Systems)
**Learning Objectives**: By the end of this chapter, you will be able to:
- Architect end-to-end Physical AI systems
- Integrate perception, planning, and control pipelines
- Deploy complete voice-to-action humanoid capabilities

## Concept Overview

This capstone integrates all modules into a complete autonomous humanoid system. The robot receives voice commands, grounds instructions in visual perception, plans action sequences via LLM, navigates using VSLAM and Nav2, manipulates objects with learned policies, and provides feedback to users. This end-to-end integration represents the Physical AI pipeline—from perception through cognition to action—that this book has progressively constructed.

## System Architecture

Complete system architecture:

```
┌──────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                            │
│  Voice Input │ Visual Feedback │ Status Display                   │
├──────────────────────────────────────────────────────────────────┤
│                     COGNITION LAYER (VLA)                         │
│  Speech-to-Command → LLM Planner → Multimodal Grounding          │
├──────────────────────────────────────────────────────────────────┤
│                    PERCEPTION LAYER (Isaac ROS)                   │
│  cuVSLAM │ Object Detection │ Depth Processing │ Scene Graph     │
├──────────────────────────────────────────────────────────────────┤
│                     PLANNING LAYER (Nav2/MoveIt)                  │
│  Global Path │ Footstep Planning │ Motion Planning │ Grasp Plan  │
├──────────────────────────────────────────────────────────────────┤
│                      CONTROL LAYER (ros2_control)                 │
│  Whole-Body Controller │ RL Policy │ Joint Controllers           │
├──────────────────────────────────────────────────────────────────┤
│                     HARDWARE / SIMULATION                         │
│  Isaac Sim │ Real Robot │ Sensors │ Actuators                    │
└──────────────────────────────────────────────────────────────────┘
```

## Data Flow and Components

**End-to-End Flow** ("Bring me the cup"):

1. **Voice**: User speaks command; ASR transcribes "bring me the cup"
2. **Intent**: NLU extracts intent=fetch, object=cup
3. **Grounding**: VLM locates cup in camera view, returns 3D position
4. **Planning**: LLM generates plan: [navigate, pick, navigate, handover]
5. **Navigation**: Nav2 plans path to cup location
6. **Locomotion**: RL policy executes walking to goal
7. **Perception**: Continuous VSLAM updates robot pose
8. **Manipulation**: MoveIt plans grasp; controller executes
9. **Return**: Navigate back to user with cup
10. **Handover**: Detect user hand, place cup
11. **Feedback**: Speak "Here is your cup"

**Integration Points**:

| Interface | From | To | Message Type |
|-----------|------|-------|--------------|
| /voice_command | Speech | LLM Planner | String |
| /grounded_object | VLM | Planner | PoseStamped |
| /goal_pose | Planner | Nav2 | PoseStamped |
| /cmd_vel | Nav2 | Controller | Twist |
| /joint_commands | Controller | Hardware | JointState |

## Example Workflow

Main coordinator node:

```python
# ROS 2 Humble | Python 3.10 | Full Integration
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from enum import Enum

class TaskState(Enum):
    IDLE = 0
    UNDERSTANDING = 1
    PLANNING = 2
    NAVIGATING = 3
    MANIPULATING = 4
    RETURNING = 5
    COMPLETE = 6

class AutonomousHumanoid(Node):
    def __init__(self):
        super().__init__('autonomous_humanoid')

        self.state = TaskState.IDLE

        # Component interfaces
        self.speech_sub = self.create_subscription(
            String, '/voice_command', self.command_callback, 10)
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Service clients (simplified)
        # self.llm_client = ...
        # self.perception_client = ...
        # self.manipulation_client = ...

        self.get_logger().info('Autonomous humanoid ready')

    def command_callback(self, msg):
        if self.state != TaskState.IDLE:
            self.get_logger().warn('Busy with current task')
            return

        self.state = TaskState.UNDERSTANDING
        self.execute_task(msg.data)

    async def execute_task(self, command):
        """Execute complete task pipeline."""
        try:
            # 1. Parse command
            self.state = TaskState.PLANNING
            plan = await self.get_plan(command)
            self.get_logger().info(f'Plan: {plan}')

            # 2. Execute each action
            for action in plan:
                if action['action'] == 'navigate':
                    self.state = TaskState.NAVIGATING
                    await self.navigate_to(action['params']['location'])

                elif action['action'] == 'pick':
                    self.state = TaskState.MANIPULATING
                    # Ground object in perception
                    pose = await self.find_object(action['params']['object'])
                    await self.pick_object(pose)

                elif action['action'] == 'place':
                    await self.place_object(action['params']['surface'])

                elif action['action'] == 'speak':
                    self.speak(action['params']['message'])

            self.state = TaskState.COMPLETE
            self.speak("Task completed")

        except Exception as e:
            self.get_logger().error(f'Task failed: {e}')
            self.speak("I encountered a problem")

        finally:
            self.state = TaskState.IDLE

    async def navigate_to(self, location):
        """Navigate to named location or pose."""
        goal = NavigateToPose.Goal()
        goal.pose = self.location_to_pose(location)

        result = await self.nav_client.send_goal_async(goal)
        await result.get_result_async()

    def location_to_pose(self, location):
        # Convert location name to PoseStamped
        # Would query semantic map
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        # ... set position/orientation
        return pose
```

Launch file for complete system:

```bash
# ROS 2 Humble | Full system launch
ros2 launch humanoid_bringup autonomous_humanoid.launch.py \
  use_sim:=true \
  enable_voice:=true \
  enable_manipulation:=true
```

## Common Failure Modes

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| Pipeline stall | Robot freezes mid-task | Implement timeouts; state monitoring |
| Cascading errors | Failures compound | Graceful degradation; error recovery |
| State inconsistency | Conflicting commands | State machine validation; locking |
| Integration latency | Slow response | Optimize pipelines; parallel execution |

## Summary

The capstone demonstrates complete Physical AI integration—voice commands flow through language understanding, visual grounding, planning, navigation, and manipulation to achieve real-world tasks. This end-to-end system represents the culmination of ROS 2 fundamentals, simulation, Isaac AI, and VLA capabilities covered across all four modules.

**Next**: [Edge Deployment](./edge-deployment)

---

## References

1. Brohan, A., et al. (2023). RT-2: Vision-Language-Action models transfer web knowledge to robotic control. *arXiv preprint*.

2. Ahn, M., et al. (2022). Do as I can, not as I say: Grounding language in robotic affordances. *CoRL*.
