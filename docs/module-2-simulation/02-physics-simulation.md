---
sidebar_position: 2
title: "Physics Simulation"
description: "Configure physics engines for humanoid robot simulation, covering contact dynamics, joint friction, and stable whole-body control."
keywords: [physics, simulation, dynamics, contact, friction, Gazebo]
---

# Physics Simulation

**Prerequisites**: Chapter 2.1 (Gazebo Environment Setup)
**Learning Objectives**: By the end of this chapter, you will be able to:
- Select and configure physics engines for humanoid simulation
- Tune contact and friction parameters for stable locomotion
- Optimize simulation step size for real-time performance

## Concept Overview

Physics simulation transforms robot models into dynamic systems governed by physical laws. For humanoid robots, accurate physics is critical—bipedal locomotion depends on precise contact dynamics, friction modeling, and joint torque limits. Gazebo supports multiple physics engines (DART, Bullet, ODE), each with trade-offs between accuracy and performance. Proper configuration prevents unrealistic behaviors like penetration, jitter, and energy gain that invalidate simulation-based development (Koenig & Howard, 2004).

## System Architecture

Physics engine integration in Gazebo:

- **Physics Engine**: Computes rigid body dynamics, collision detection, constraint solving
  - **DART**: High accuracy, stable for articulated robots, slower
  - **Bullet**: Good balance of speed and accuracy, gaming heritage
  - **ODE**: Fast, less accurate for complex contacts
- **Collision Detection**: Geometric intersection tests between collision shapes
- **Constraint Solver**: Resolves joint constraints, contact forces, friction
- **Integrator**: Advances simulation state through time

For humanoid robots, DART is typically preferred due to its robust handling of high-DOF articulated structures and stable contact constraint solving.

## Data Flow and Components

**Physics Step Cycle**:
1. Apply external forces and joint commands
2. Detect collisions between bodies
3. Generate contact constraints at collision points
4. Solve joint and contact constraints simultaneously
5. Integrate velocities and positions
6. Publish updated state to subscribers

**Key Parameters**:
- `max_step_size`: Physics timestep (typically 0.001s for humanoids)
- `real_time_factor`: Target speed relative to wall clock
- `friction_coefficient`: Surface friction (μ ≈ 0.8 for rubber on concrete)
- `contact_stiffness/damping`: Soft contact model parameters
- `solver_iterations`: Constraint solver accuracy vs. speed

## Example Workflow

Physics configuration for stable humanoid simulation:

```xml
<!-- Gazebo Fortress | SDF 1.9 | DART Physics -->
<physics type="dart">
  <!-- Small timestep for humanoid stability -->
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1.0</real_time_factor>

  <dart>
    <!-- Constraint solver settings -->
    <solver>
      <solver_type>dantzig</solver_type>
    </solver>
    <collision_detector>bullet</collision_detector>
  </dart>
</physics>

<!-- Ground surface with friction -->
<collision name="ground_collision">
  <geometry><plane><size>100 100</size></plane></geometry>
  <surface>
    <friction>
      <ode>
        <mu>0.8</mu>
        <mu2>0.8</mu2>
      </ode>
    </friction>
    <contact>
      <ode>
        <kp>1e6</kp>    <!-- Contact stiffness -->
        <kd>100</kd>    <!-- Contact damping -->
      </ode>
    </contact>
  </surface>
</collision>
```

Testing friction with a simple slope test:

```python
# ROS 2 Humble | Python 3.10
# Verify friction: robot should not slide on slope < arctan(μ)
import math
mu = 0.8  # friction coefficient
max_slope = math.degrees(math.atan(mu))  # ~38.7 degrees
print(f"Robot should hold on slopes up to {max_slope:.1f} degrees")
```

## Common Failure Modes

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| Penetration | Bodies pass through each other | Increase solver iterations; reduce step size |
| Jitter/vibration | Robot shakes at rest | Tune contact stiffness/damping; check inertias |
| Energy gain | Robot accelerates without input | Reduce step size; check joint damping |
| Slow simulation | Real-time factor much less than 1 | Simplify collision geometry; use faster engine |

## Summary

Physics simulation accuracy directly impacts the validity of humanoid robot testing. Proper engine selection, timestep configuration, and contact parameter tuning ensure stable, realistic behavior. DART with small timesteps provides the robustness needed for bipedal locomotion development.

**Next**: [URDF and SDF Usage](./urdf-sdf-usage)

---

## References

1. Koenig, N., & Howard, A. (2004). Design and use paradigms for Gazebo, an open-source multi-robot simulator. *IEEE/RSJ International Conference on Intelligent Robots and Systems*, 3, 2149-2154.

2. Open Robotics. (2023). *Gazebo Fortress documentation - Physics*. https://gazebosim.org/docs/fortress
