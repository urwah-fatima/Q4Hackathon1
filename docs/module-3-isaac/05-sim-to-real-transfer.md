---
sidebar_position: 5
title: "Chapter 3.5: Sim-to-Real Transfer"
description: "Transfer learned policies from simulation to physical humanoid robots using domain adaptation and system identification."
keywords: [sim-to-real, transfer learning, domain adaptation, robotics, deployment]
---

# Chapter 3.5: Sim-to-Real Transfer

**Prerequisites**: Chapter 3.4 (Reinforcement Learning)
**Learning Objectives**: By the end of this chapter, you will be able to:
- Apply domain randomization for robust policy transfer
- Perform system identification to align simulation with hardware
- Deploy trained policies on physical humanoid robots

## Concept Overview

Sim-to-real transfer bridges the gap between simulated training and physical deployment. Policies trained purely in simulation often fail on real robots due to differences in dynamics, sensing, and actuation. Successful transfer requires domain randomization (training across varied simulation parameters), system identification (tuning simulation to match reality), and deployment infrastructure. For humanoid robots, this challenge is acute—bipedal stability demands precise dynamics modeling (Tan et al., 2018).

## System Architecture

Transfer pipeline components:

- **Domain Randomization**: Vary physics parameters during training
- **System Identification**: Measure real robot, tune simulation
- **Policy Distillation**: Compress policy for embedded deployment
- **Safety Wrapper**: Limit actions within safe bounds
- **Fallback Controller**: Emergency stabilization if policy fails
- **Hardware Abstraction**: Consistent interface across sim and real

The architecture maintains identical observation/action interfaces between simulation and reality, with safety systems wrapping the learned policy.

## Data Flow and Components

**Transfer Workflow**:
1. Train policy with aggressive domain randomization
2. Collect calibration data from real robot
3. Perform system identification on key parameters
4. Fine-tune policy in calibrated simulation (optional)
5. Deploy policy with safety wrapper on hardware
6. Monitor performance, iterate

**Domain Randomization Parameters**:

| Parameter | Randomization Range | Effect |
|-----------|-------------------|--------|
| Mass | ±15% | Robustness to payload |
| Friction | ±30% | Terrain adaptation |
| Motor strength | ±10% | Actuator variation |
| Latency | 0-50ms | Control delay tolerance |
| Sensor noise | ±20% | Measurement uncertainty |
| Joint damping | ±20% | Dynamic response |

## Example Workflow

Domain randomization configuration:

```python
# Isaac Gym 1.0.x | Python 3.8 | Domain Randomization
class DomainRandomizationConfig:
    """Randomization ranges for sim-to-real transfer."""

    # Randomize at episode reset
    randomize_friction = True
    friction_range = [0.5, 1.25]  # multiplier on nominal

    randomize_mass = True
    mass_range = [0.85, 1.15]  # multiplier on nominal

    randomize_motor_strength = True
    motor_strength_range = [0.9, 1.1]

    # Randomize during episode
    push_robots = True
    push_interval_s = 8
    push_force_range = [50, 100]  # Newtons

    # Observation noise
    add_noise = True
    noise_scales = {
        'joint_pos': 0.01,  # radians
        'joint_vel': 0.1,   # rad/s
        'imu_ang_vel': 0.05,  # rad/s
        'imu_lin_acc': 0.1,   # m/s²
    }

    # Action delay simulation
    action_delay_range = [0, 2]  # timesteps

def apply_domain_randomization(env, config):
    """Apply randomization to environment."""
    if config.randomize_friction:
        friction = torch.empty(env.num_envs).uniform_(*config.friction_range)
        env.set_friction(friction)

    if config.randomize_mass:
        mass_scale = torch.empty(env.num_envs).uniform_(*config.mass_range)
        env.scale_masses(mass_scale)
```

Deployment with safety wrapper:

```python
# ROS 2 Humble | Python 3.10 | Policy Deployment
import torch
import rclpy
from rclpy.node import Node

class SafePolicyDeployer(Node):
    """Deploy RL policy with safety constraints."""

    def __init__(self, policy_path):
        super().__init__('policy_deployer')

        # Load trained policy
        self.policy = torch.jit.load(policy_path)
        self.policy.eval()

        # Safety limits
        self.max_joint_velocity = 2.0  # rad/s
        self.max_torque = 50.0  # Nm

        self.get_logger().info('Policy deployed with safety wrapper')

    def compute_action(self, observation):
        with torch.no_grad():
            action = self.policy(observation)

        # Clamp to safe bounds
        action = torch.clamp(action, -self.max_torque, self.max_torque)

        # Rate limit for smooth motion
        action = self.rate_limit(action)

        return action

    def rate_limit(self, action, max_delta=0.1):
        if hasattr(self, 'prev_action'):
            delta = action - self.prev_action
            delta = torch.clamp(delta, -max_delta, max_delta)
            action = self.prev_action + delta
        self.prev_action = action.clone()
        return action
```

## Common Failure Modes

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| Dynamics mismatch | Robot falls immediately | System identification; increase randomization |
| Latency sensitivity | Oscillations, instability | Add latency randomization; reduce control rate |
| Observation gap | Policy confused by real sensors | Match sensor models; add noise in training |
| Safety violation | Dangerous joint velocities | Add safety wrapper; tune action limits |

## Summary

Sim-to-real transfer transforms simulation-trained policies into deployable controllers. Domain randomization builds robustness during training, while system identification aligns simulation with hardware specifics. Safety wrappers and fallback systems ensure reliable operation during deployment on physical humanoid robots.

**Next**: [ROS 2 and Isaac Integration](./ros2-isaac-integration)

---

## References

1. Tan, J., Zhang, T., Coumans, E., Iscen, A., Bai, Y., Hafner, D., Bohez, S., & Vanhoucke, V. (2018). Sim-to-real: Learning agile locomotion for quadruped robots. *RSS*.

2. NVIDIA. (2023). *Isaac Sim documentation - Sim-to-Real*. https://docs.omniverse.nvidia.com/isaacsim/latest/
