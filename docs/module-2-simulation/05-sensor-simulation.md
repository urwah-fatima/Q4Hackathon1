---
sidebar_position: 5
title: "Chapter 2.5: Sensor Simulation"
description: "Simulate cameras, LiDAR, IMU, and force sensors for humanoid robots in Gazebo with realistic noise models."
keywords: [sensors, simulation, LiDAR, camera, IMU, Gazebo, robotics]
---

# Chapter 2.5: Sensor Simulation

**Prerequisites**: Chapter 2.4 (Unity Visualization)
**Learning Objectives**: By the end of this chapter, you will be able to:
- Configure camera, LiDAR, and IMU sensors in Gazebo
- Apply realistic noise models to simulated sensor data
- Bridge sensor topics to ROS 2 for perception pipeline testing

## Concept Overview

Sensor simulation enables testing perception algorithms without physical hardware. Gazebo models common robotic sensors—cameras, LiDAR, IMU, force/torque sensors—with configurable noise characteristics. For humanoid robots, accurate sensor simulation is essential for developing vision systems, balance controllers, and contact detection. Realistic noise models prevent over-optimistic algorithm performance that fails on real hardware (Koenig & Howard, 2004).

## System Architecture

Gazebo sensor simulation components:

- **Sensor Plugins**: Generate data streams matching real sensor behavior
- **Rendering Sensors**: Cameras, depth cameras use GPU-accelerated rendering
- **Ray Sensors**: LiDAR, sonar use ray casting against collision geometry
- **Physics Sensors**: IMU, force/torque derive from physics engine state
- **Noise Models**: Gaussian, bias, drift applied to sensor outputs
- **ROS Bridge**: Publishes sensor data to standard ROS 2 message types

Sensor data flows from physics/rendering engines through plugins to the ROS bridge, appearing as standard topics for perception nodes.

## Data Flow and Components

**Sensor Pipeline**:
1. Physics engine updates world state
2. Rendering engine generates camera/depth images
3. Sensor plugins sample world state at configured rate
4. Noise models corrupt ideal measurements
5. ros_gz_bridge publishes to ROS 2 topics
6. Perception nodes process as if from real hardware

**Common Humanoid Sensors**:

| Sensor | Message Type | Use Case |
|--------|-------------|----------|
| RGB Camera | `sensor_msgs/Image` | Visual perception, object detection |
| Depth Camera | `sensor_msgs/PointCloud2` | 3D mapping, obstacle detection |
| IMU | `sensor_msgs/Imu` | Balance, orientation estimation |
| Force/Torque | `geometry_msgs/WrenchStamped` | Contact detection, manipulation |
| Joint Encoder | `sensor_msgs/JointState` | Proprioception, control feedback |

## Example Workflow

Configuring a head-mounted camera with depth:

```xml
<!-- Gazebo Fortress | SDF 1.9 | RGBD Camera -->
<sensor name="head_camera" type="rgbd_camera">
  <pose>0.1 0 0.05 0 0 0</pose>
  <update_rate>30</update_rate>

  <camera>
    <horizontal_fov>1.047</horizontal_fov>  <!-- 60 degrees -->
    <image>
      <width>640</width>
      <height>480</height>
      <format>R8G8B8</format>
    </image>
    <clip>
      <near>0.1</near>
      <far>10.0</far>
    </clip>
    <depth_camera>
      <clip>
        <near>0.1</near>
        <far>10.0</far>
      </clip>
    </depth_camera>
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.007</stddev>
    </noise>
  </camera>

  <plugin filename="libgazebo_ros_camera.so" name="camera_plugin">
    <ros>
      <remapping>image_raw:=/head_camera/color/image_raw</remapping>
      <remapping>depth/image_raw:=/head_camera/depth/image_raw</remapping>
      <remapping>camera_info:=/head_camera/color/camera_info</remapping>
    </ros>
  </plugin>
</sensor>
```

IMU configuration with realistic noise:

```xml
<!-- Gazebo Fortress | SDF 1.9 | IMU Sensor -->
<sensor name="imu_sensor" type="imu">
  <update_rate>100</update_rate>
  <imu>
    <angular_velocity>
      <x><noise type="gaussian"><mean>0</mean><stddev>0.01</stddev></noise></x>
      <y><noise type="gaussian"><mean>0</mean><stddev>0.01</stddev></noise></y>
      <z><noise type="gaussian"><mean>0</mean><stddev>0.01</stddev></noise></z>
    </angular_velocity>
    <linear_acceleration>
      <x><noise type="gaussian"><mean>0</mean><stddev>0.1</stddev></noise></x>
      <y><noise type="gaussian"><mean>0</mean><stddev>0.1</stddev></noise></y>
      <z><noise type="gaussian"><mean>0</mean><stddev>0.1</stddev></noise></z>
    </linear_acceleration>
  </imu>
</sensor>
```

## Common Failure Modes

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| No sensor output | Topic exists but no messages | Check update_rate > 0; verify plugin loaded |
| Frame ID missing | TF lookup failures | Configure frame_name in plugin |
| Unrealistic noise | Algorithms fail on real data | Calibrate noise to match real sensor specs |
| Low update rate | Perception lag | Balance rate vs. computational load |

## Summary

Sensor simulation enables comprehensive perception development without hardware. Configuring realistic noise models—matching manufacturer specifications—ensures algorithms generalize to real sensors. The combination of visual, depth, inertial, and force sensing provides humanoid robots with the sensory foundation for autonomous operation.

**Next**: [Validation Strategies](./validation-strategies)

---

## References

1. Koenig, N., & Howard, A. (2004). Design and use paradigms for Gazebo, an open-source multi-robot simulator. *IEEE/RSJ International Conference on Intelligent Robots and Systems*, 3, 2149-2154.

2. Open Robotics. (2023). *Gazebo Fortress documentation - Sensors*. https://gazebosim.org/docs/fortress
