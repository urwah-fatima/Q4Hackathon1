---
sidebar_position: 3
title: "URDF and SDF Usage"
description: "Compare URDF and SDF robot description formats, covering conversion workflows and best practices for humanoid simulation."
keywords: [URDF, SDF, robot description, conversion, Gazebo, ROS 2]
---

# URDF and SDF Usage

**Prerequisites**: Chapter 2.2 (Physics Simulation)
**Learning Objectives**: By the end of this chapter, you will be able to:
- Distinguish between URDF and SDF capabilities and use cases
- Convert URDF models to SDF for Gazebo simulation
- Apply Gazebo-specific extensions to URDF models

## Concept Overview

Robot description formats define the structure, kinematics, and dynamics of robots. URDF (Unified Robot Description Format) is the ROS standard, designed for kinematic chains and controller configuration. SDF (Simulation Description Format) is Gazebo's native format, supporting richer simulation features like sensors, plugins, and nested models. For humanoid development, understanding both formats—and conversion between them—is essential for seamless ROS 2 to Gazebo workflows (Open Robotics, 2023).

## System Architecture

**URDF Capabilities**:
- Kinematic tree structure (links, joints)
- Visual and collision geometry
- Inertial properties (mass, inertia tensor)
- Joint limits, dynamics (friction, damping)
- Transmission definitions for ros2_control

**SDF Additional Capabilities**:
- Multiple robots in one file
- World-level elements (lights, physics, plugins)
- Advanced sensor definitions (noise models, update rates)
- Model composition and nesting
- Actor animations and trajectories

The ROS 2 ecosystem uses URDF for `robot_state_publisher` and controller configuration, while Gazebo prefers SDF for simulation.

## Data Flow and Components

**URDF to Gazebo Pipeline**:
1. Author URDF with `<gazebo>` extension tags
2. `robot_state_publisher` publishes `/robot_description`
3. `ros_gz_sim` spawn service converts URDF to SDF internally
4. Gazebo loads converted model with plugins attached
5. Alternatively, use `gz sdf -p robot.urdf > robot.sdf` for offline conversion

**Key Differences**:

| Feature | URDF | SDF |
|---------|------|-----|
| Root element | `<robot>` | `<model>` or `<world>` |
| Multiple models | No | Yes |
| Sensor plugins | Via `<gazebo>` | Native `<sensor>` |
| World description | No | Yes |
| Nested models | No | Yes |

## Example Workflow

URDF with Gazebo extensions for simulation:

```xml
<!-- ROS 2 Humble | URDF 1.0 with Gazebo Extensions -->
<?xml version="1.0"?>
<robot name="humanoid_leg">

  <link name="thigh">
    <visual>
      <geometry><cylinder radius="0.04" length="0.4"/></geometry>
    </visual>
    <collision>
      <geometry><cylinder radius="0.04" length="0.4"/></geometry>
    </collision>
    <inertial>
      <mass value="3.0"/>
      <inertia ixx="0.04" ixy="0" ixz="0" iyy="0.04" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Gazebo-specific extensions -->
  <gazebo reference="thigh">
    <material>Gazebo/Blue</material>
    <mu1>0.8</mu1>
    <mu2>0.8</mu2>
  </gazebo>

  <joint name="hip_pitch" type="revolute">
    <parent link="pelvis"/>
    <child link="thigh"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="0.5" effort="100" velocity="5"/>
  </joint>

  <!-- Gazebo joint plugin -->
  <gazebo>
    <plugin filename="libgazebo_ros2_control.so" name="gazebo_ros2_control">
      <robot_param>robot_description</robot_param>
      <robot_param_node>robot_state_publisher</robot_param_node>
    </plugin>
  </gazebo>

</robot>
```

Converting URDF to SDF:

```bash
# Gazebo Fortress | CLI conversion
gz sdf -p humanoid.urdf > humanoid.sdf

# Verify conversion
gz sdf -k humanoid.sdf  # Check for errors
```

## Common Failure Modes

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| Missing inertials | Conversion fails | Add `<inertial>` to all non-fixed links |
| Unsupported URDF tags | Warning messages | Use `<gazebo>` extensions for sim-specific features |
| Mesh path errors | Visual/collision missing | Use `package://` or absolute paths |
| Plugin not found | Gazebo errors on spawn | Verify plugin library installed and path correct |

## Summary

URDF and SDF serve complementary roles—URDF for ROS 2 tooling compatibility, SDF for advanced Gazebo features. The `<gazebo>` extension mechanism bridges the gap, allowing URDF-based workflows to access simulation capabilities. For complex humanoid robots, maintaining URDF as the source of truth with Gazebo extensions provides the best balance of ROS integration and simulation fidelity.

**Next**: [Unity Visualization](./unity-visualization)

---

## References

1. Open Robotics. (2023). *ROS 2 Humble documentation - URDF*. https://docs.ros.org/en/humble/

2. Open Robotics. (2023). *SDFormat specification*. http://sdformat.org/spec
