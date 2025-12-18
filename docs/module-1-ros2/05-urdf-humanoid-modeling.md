---
sidebar_position: 5
title: "URDF for Humanoid Modeling"
description: "Define humanoid robot models using URDF, covering links, joints, kinematic chains, and physical properties for simulation and control."
keywords: [URDF, humanoid, robot model, links, joints, ROS 2]
---

# URDF for Humanoid Modeling

**Prerequisites**: Chapter 1.4 (Python Agents with rclpy)
**Learning Objectives**: By the end of this chapter, you will be able to:
- Define robot structure using URDF links and joints
- Model humanoid kinematic chains (arms, legs, torso)
- Specify visual, collision, and inertial properties

## Concept Overview

Unified Robot Description Format (URDF) is an XML specification for describing robot structure. It defines the kinematic and dynamic properties required for simulation, visualization, and control. For humanoid robots, URDF captures the complex articulated structure—dozens of links connected by joints forming kinematic chains for arms, legs, torso, and head. A well-defined URDF is foundational; it enables motion planning, physics simulation in Gazebo, and real-time control through joint state interfaces (Open Robotics, 2023).

## System Architecture

URDF models robots as a tree of rigid bodies:

- **Links**: Rigid bodies with visual geometry (for rendering), collision geometry (for physics), and inertial properties (mass, center of mass, inertia tensor)
- **Joints**: Connections between links specifying motion type and limits
  - `revolute`: Rotation with limits (elbow, knee)
  - `continuous`: Unlimited rotation (wheel)
  - `prismatic`: Linear motion (linear actuator)
  - `fixed`: No motion (sensor mount)
- **Kinematic Chains**: Series of links/joints forming functional units

A humanoid URDF typically includes chains for: torso, left/right arms (shoulder, elbow, wrist), left/right legs (hip, knee, ankle), and head (neck, pan/tilt).

## Data Flow and Components

**URDF Processing Pipeline**:
1. Author URDF XML (or generate via xacro macros)
2. Load via `robot_state_publisher` node
3. Publish transforms to `/tf` topic
4. Visualization tools (RViz) render robot state
5. Controllers read joint limits and dynamics from parameter server

**Key Elements**:
- `<robot>`: Root element with robot name
- `<link>`: Defines body segment with `<visual>`, `<collision>`, `<inertial>`
- `<joint>`: Connects parent/child links with type, axis, limits
- `<material>`: Defines colors for visualization
- `<gazebo>`: Extensions for simulation (friction, sensors)

## Example Workflow

A simplified URDF for a humanoid arm:

```xml
<!-- ROS 2 Humble | URDF 1.0 -->
<?xml version="1.0"?>
<robot name="humanoid_arm">

  <link name="shoulder">
    <visual>
      <geometry><cylinder radius="0.05" length="0.1"/></geometry>
      <material name="blue"><color rgba="0 0 0.8 1"/></material>
    </visual>
    <collision>
      <geometry><cylinder radius="0.05" length="0.1"/></geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <link name="upper_arm">
    <visual>
      <geometry><box size="0.05 0.05 0.3"/></geometry>
    </visual>
    <inertial>
      <mass value="0.8"/>
      <inertia ixx="0.006" ixy="0" ixz="0" iyy="0.006" iyz="0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="shoulder_pitch" type="revolute">
    <parent link="shoulder"/>
    <child link="upper_arm"/>
    <origin xyz="0 0 -0.05" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="50" velocity="2.0"/>
  </joint>

</robot>
```

## Common Failure Modes

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| Missing inertia | Simulation instability | Always define realistic inertial properties |
| Incorrect joint limits | Unrealistic motion | Verify limits against hardware specifications |
| Mesh file not found | Visual/collision missing | Use absolute paths or proper package:// URIs |
| Disconnected tree | Parser errors | Ensure all links connect via joints to base |

## Summary

URDF provides the structural blueprint for humanoid robots in ROS 2. Accurate modeling of links, joints, and physical properties enables realistic simulation and proper control. The URDF serves as the single source of truth for robot geometry across visualization, planning, and control subsystems.

**Next**: [Launch Files and Parameters](./launch-files-parameters)

---

## References

1. Open Robotics. (2023). *ROS 2 Humble documentation - URDF*. https://docs.ros.org/en/humble/

2. Quigley, M., Conley, K., Gerkey, B., Faust, J., Foote, T., Leibs, J., Wheeler, R., & Ng, A. Y. (2009). ROS: an open-source Robot Operating System. *ICRA Workshop on Open Source Software*, 3(3.2), 5.
