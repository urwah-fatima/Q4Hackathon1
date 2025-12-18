---
sidebar_position: 6
title: "Launch Files and Parameters"
description: "Orchestrate complex ROS 2 humanoid systems using Python launch files, parameter configuration, and composable node patterns."
keywords: [ROS 2, launch files, parameters, configuration, YAML]
---

# Launch Files and Parameters

**Prerequisites**: Chapter 1.5 (URDF for Humanoid Modeling)
**Learning Objectives**: By the end of this chapter, you will be able to:
- Create Python-based launch files for multi-node systems
- Configure nodes using parameter files and launch arguments
- Apply composition patterns for humanoid robot deployment

## Concept Overview

Launch files orchestrate the startup of complex ROS 2 systems. A humanoid robot may require dozens of nodes—drivers, perception, planning, control—each with specific parameters. ROS 2's Python-based launch system provides programmatic control over node configuration, conditional logic, and composition. Combined with YAML parameter files, launch files enable reproducible deployment configurations for development, simulation, and production environments (Open Robotics, 2023).

## System Architecture

The ROS 2 launch system components:

- **LaunchDescription**: Container for launch actions
- **Node Action**: Launches an executable with namespace, parameters, and remappings
- **IncludeLaunchDescription**: Composes launch files hierarchically
- **DeclareLaunchArgument**: Defines runtime-configurable arguments
- **LaunchConfiguration**: References declared arguments
- **Substitutions**: Dynamic value resolution (environment variables, paths)

For humanoid robots, launch files typically follow a hierarchy: top-level robot launch includes subsystem launches (perception, locomotion, manipulation), each including component-specific launches. This modular structure enables testing subsystems independently.

## Data Flow and Components

**Launch Execution Flow**:
1. Parse launch file, resolve substitutions
2. Process launch arguments from command line
3. Execute actions in declaration order
4. Load parameter files, pass to nodes
5. Start nodes, apply remappings
6. Monitor node lifecycle

**Parameter Sources** (priority order):
1. Command-line overrides (`--ros-args -p param:=value`)
2. Launch file parameter dictionaries
3. YAML parameter files
4. Node-declared defaults

Parameters support types: bool, int, double, string, and arrays thereof.

## Example Workflow

A launch file for a humanoid robot system:

```python
# ROS 2 Humble | Python 3.10
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Declare arguments
    use_sim = DeclareLaunchArgument(
        'use_sim', default_value='true',
        description='Use simulation clock'
    )

    robot_config = PathJoinSubstitution([
        FindPackageShare('humanoid_bringup'), 'config', 'robot_params.yaml'
    ])

    # Robot state publisher
    robot_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[robot_config],
        arguments=['--ros-args', '--log-level', 'info']
    )

    # Joint state broadcaster
    joint_state = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim')}]
    )

    # Humanoid controller
    controller = Node(
        package='humanoid_control',
        executable='whole_body_controller',
        parameters=[robot_config, {'use_sim_time': LaunchConfiguration('use_sim')}],
        remappings=[('/cmd_vel', '/humanoid/cmd_vel')]
    )

    return LaunchDescription([
        use_sim,
        robot_state_pub,
        joint_state,
        controller
    ])
```

**Associated parameter file** (`robot_params.yaml`):

```yaml
# ROS 2 Humble | YAML parameters
robot_state_publisher:
  ros__parameters:
    robot_description: ""
    publish_frequency: 50.0

whole_body_controller:
  ros__parameters:
    control_rate: 100.0
    joint_limits_enforced: true
```

## Common Failure Modes

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| Parameter not found | Node crashes on startup | Declare all parameters with defaults |
| Package not found | Launch file fails | Verify package installed; check `FindPackageShare` |
| Argument not declared | Substitution error | Declare all `LaunchConfiguration` sources |
| Circular include | Infinite loop on launch | Review include hierarchy; avoid cycles |

## Summary

Launch files are the deployment specification for ROS 2 humanoid systems. Python's flexibility enables conditional logic, composition, and integration with external configuration. Combined with parameter files, launch configurations provide reproducible, version-controlled deployment across development and production environments. This concludes Module 1—you now have the ROS 2 foundation for building humanoid robot systems.

**Next**: [Module 2: Gazebo Environment Setup](../module-2-simulation/gazebo-environment-setup)

---

## References

1. Open Robotics. (2023). *ROS 2 Humble documentation - Launch*. https://docs.ros.org/en/humble/

2. Macenski, S., Foote, T., Gerkey, B., Lalancette, C., & Woodall, W. (2022). Robot Operating System 2: Design, architecture, and uses in the wild. *Science Robotics*, 7(66), eabm6074.
