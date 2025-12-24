---
sidebar_position: 3
title: "Chapter 3.3: Nav2 for Humanoid Navigation"
description: "Configure the ROS 2 Navigation Stack (Nav2) for bipedal humanoid locomotion with custom planners and controllers."
keywords: [Nav2, navigation, path planning, humanoid, ROS 2, locomotion]
---

# Chapter 3.3: Nav2 for Humanoid Navigation

**Prerequisites**: Chapter 3.2 (Isaac ROS and VSLAM)
**Learning Objectives**: By the end of this chapter, you will be able to:
- Configure Nav2 for humanoid-specific locomotion constraints
- Implement custom planners accounting for bipedal stability
- Integrate footstep planning with Nav2's behavior tree architecture

## Concept Overview

Nav2 (Navigation 2) is the ROS 2 navigation stack providing autonomous navigation capabilities—path planning, obstacle avoidance, and recovery behaviors. For humanoid robots, Nav2 requires adaptation: unlike wheeled robots, humanoids have stability constraints, discrete footstep placement, and cannot instantaneously change direction. This chapter covers Nav2 configuration for bipedal locomotion, including custom costmap layers and footstep-aware planning (Macenski et al., 2020).

## System Architecture

Nav2 architecture for humanoids:

- **BT Navigator**: Behavior tree orchestrating navigation tasks
- **Planner Server**: Computes global paths (NavFn, Smac, custom)
- **Controller Server**: Follows paths locally (DWB, MPPI, custom)
- **Costmap 2D**: Maintains obstacle representation from sensors
- **Recovery Server**: Handles stuck/failure situations
- **Footstep Planner** (custom): Discrete foot placement planning

Unlike wheeled robots using continuous velocity commands, humanoids require translation to footstep sequences or whole-body trajectories.

## Data Flow and Components

**Navigation Pipeline**:
1. Receive goal pose from operator or task planner
2. Global planner computes path avoiding static obstacles
3. Footstep planner converts path to discrete foot placements
4. Local controller executes footsteps while avoiding dynamic obstacles
5. VSLAM provides localization updates
6. Behavior tree handles replanning and recovery

**Humanoid-Specific Costmap Layers**:

| Layer | Purpose |
|-------|---------|
| Static | Pre-mapped obstacles |
| Obstacle | Dynamic obstacles from sensors |
| Inflation | Safe distance buffer |
| Footstep Validity | Terrain suitable for stepping |
| Stability Margin | Areas requiring careful balance |

## Example Workflow

Nav2 configuration for humanoid robot:

```yaml
# ROS 2 Humble | Nav2 1.1.x | YAML configuration
bt_navigator:
  ros__parameters:
    default_nav_to_pose_bt_xml: HumanoidNavigateToPose.xml
    plugin_lib_names:
      - nav2_compute_path_to_pose_action_bt_node
      - nav2_follow_path_action_bt_node
      - nav2_recovery_node_bt_node

planner_server:
  ros__parameters:
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_smac_planner/SmacPlannerHybrid"
      tolerance: 0.25
      allow_unknown: true
      max_iterations: 10000
      # Humanoid turning radius (larger than wheeled)
      minimum_turning_radius: 0.5

controller_server:
  ros__parameters:
    controller_plugins: ["FollowPath"]
    FollowPath:
      plugin: "nav2_regulated_pure_pursuit_controller::RegulatedPurePursuitController"
      # Slower speeds for bipedal stability
      max_linear_vel: 0.3
      max_angular_vel: 0.5
      # Lookahead for stable walking
      lookahead_dist: 1.0
```

Custom footstep interface node:

```python
# ROS 2 Humble | Python 3.10 | rclpy
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

class FootstepConverter(Node):
    """Convert Nav2 path to footstep sequence."""

    def __init__(self):
        super().__init__('footstep_converter')
        self.path_sub = self.create_subscription(
            Path, '/plan', self.path_callback, 10)
        self.footstep_pub = self.create_publisher(
            Path, '/footstep_plan', 10)
        self.step_length = 0.3  # meters

    def path_callback(self, path_msg):
        # Convert continuous path to discrete footsteps
        footsteps = self.discretize_path(path_msg, self.step_length)
        self.footstep_pub.publish(footsteps)
```

## Common Failure Modes

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| Unstable gait | Robot wobbles during turns | Reduce angular velocity; add stability constraints |
| Path infeasible | Planner returns no path | Increase tolerance; check footstep validity layer |
| Recovery loops | Repeated recovery attempts | Tune recovery behaviors for bipedal motion |
| Localization drift | Robot veers off path | Integrate VSLAM tightly; add drift compensation |

## Summary

Nav2 provides a robust framework for humanoid navigation when properly configured for bipedal constraints. Custom costmap layers, reduced velocities, and footstep planning integration enable safe autonomous navigation. The behavior tree architecture supports complex recovery strategies essential for real-world humanoid deployment.

**Next**: [Reinforcement Learning](./reinforcement-learning)

---

## References

1. Macenski, S., Martín, F., White, R., & Clavero, J. G. (2020). The Marathon 2: A navigation system. *IEEE/RSJ International Conference on Intelligent Robots and Systems*.

2. NVIDIA. (2023). *Isaac ROS Nav2 documentation*. https://nvidia-isaac-ros.github.io/
