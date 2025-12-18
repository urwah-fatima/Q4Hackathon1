---
sidebar_position: 1
title: "Gazebo Environment Setup"
description: "Configure Gazebo Fortress simulation environments for humanoid robotics, including world files, models, and ROS 2 integration."
keywords: [Gazebo, simulation, environment, world files, ROS 2, robotics]
---

# Gazebo Environment Setup

**Prerequisites**: Module 1 (ROS 2 Fundamentals)
**Learning Objectives**: By the end of this chapter, you will be able to:
- Install and configure Gazebo Fortress for ROS 2 Humble
- Create world files with terrain, lighting, and physics properties
- Import robot models and configure ROS 2 bridge communication

## Concept Overview

Gazebo is the primary open-source simulator for ROS 2 robotics development. Gazebo Fortress (the Ignition generation) provides high-fidelity physics, sensor simulation, and tight ROS 2 integration through the `ros_gz` bridge. For humanoid robots, Gazebo enables safe testing of locomotion algorithms, manipulation tasks, and perception pipelines before deployment on physical hardware. The simulator's modular plugin architecture supports custom physics engines, renderers, and sensors (Koenig & Howard, 2004).

## System Architecture

Gazebo Fortress architecture comprises:

- **Gazebo Server (gz sim -s)**: Headless physics simulation engine
- **Gazebo GUI (gz sim -g)**: Visualization and interaction client
- **World Files (.sdf)**: XML descriptions of environments, models, and plugins
- **Model Database**: Local and Fuel-hosted reusable robot/object models
- **ROS 2 Bridge (ros_gz_bridge)**: Bidirectional message translation between Gazebo and ROS 2

The server-client separation enables distributed simulation—physics computation on one machine, visualization on another. For humanoid development, this allows running computationally intensive whole-body dynamics on powerful servers while monitoring from development workstations.

## Data Flow and Components

**Simulation Initialization Flow**:
1. Launch Gazebo server with world file
2. World parser loads SDF, initializes physics engine
3. Models spawn with plugins attached (sensors, controllers)
4. ros_gz_bridge starts, subscribes to Gazebo topics
5. ROS 2 nodes interact with simulation via bridge

**Key World File Components**:
- `<world>`: Container for scene, physics, models
- `<physics>`: Engine selection, step size, real-time factor
- `<scene>`: Lighting, shadows, ambient occlusion
- `<include>`: Reference to model from database
- `<plugin>`: Attach functionality (sensors, controllers)

## Example Workflow

Creating a basic humanoid testing environment:

```xml
<!-- Gazebo Fortress | SDF 1.9 -->
<?xml version="1.0"?>
<sdf version="1.9">
  <world name="humanoid_lab">

    <!-- Physics configuration -->
    <physics type="dart">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>

    <!-- Lighting -->
    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
    </light>

    <!-- Ground plane -->
    <model name="ground">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry><plane><size>100 100</size></plane></geometry>
        </collision>
        <visual name="visual">
          <geometry><plane><size>100 100</size></plane></geometry>
        </visual>
      </link>
    </model>

    <!-- Include humanoid from model database -->
    <include>
      <uri>model://humanoid_robot</uri>
      <pose>0 0 1.0 0 0 0</pose>
    </include>

  </world>
</sdf>
```

Launch with ROS 2 integration:

```bash
# Gazebo Fortress | ROS 2 Humble
ros2 launch ros_gz_sim gz_sim.launch.py world_sdf_file:=humanoid_lab.sdf
```

## Common Failure Modes

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| Model not found | Empty world, spawn errors | Check model paths; verify Fuel connectivity |
| Physics instability | Robot explodes/vibrates | Reduce step size; check inertia values |
| Bridge not connecting | No ROS 2 topics visible | Verify bridge launch; check topic mappings |
| Real-time factor < 1 | Simulation runs slowly | Reduce model complexity; use faster physics engine |

## Summary

Gazebo Fortress provides the simulation foundation for humanoid robot development. Proper world configuration—physics settings, lighting, and model placement—ensures realistic testing environments. The ROS 2 bridge enables seamless integration with perception and control nodes developed in Module 1.

**Next**: [Physics Simulation](./physics-simulation)

---

## References

1. Koenig, N., & Howard, A. (2004). Design and use paradigms for Gazebo, an open-source multi-robot simulator. *IEEE/RSJ International Conference on Intelligent Robots and Systems*, 3, 2149-2154.

2. Open Robotics. (2023). *Gazebo Fortress documentation*. https://gazebosim.org/docs/fortress
