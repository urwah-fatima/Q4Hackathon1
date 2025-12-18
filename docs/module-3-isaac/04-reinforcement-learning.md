---
sidebar_position: 4
title: "Reinforcement Learning"
description: "Train humanoid locomotion and manipulation policies using reinforcement learning in Isaac Gym and Isaac Sim."
keywords: [reinforcement learning, RL, locomotion, policy, Isaac Gym, humanoid]
---

# Reinforcement Learning

**Prerequisites**: Chapter 3.3 (Nav2 for Humanoid Navigation)
**Learning Objectives**: By the end of this chapter, you will be able to:
- Configure Isaac Gym for massively parallel humanoid training
- Design reward functions for bipedal locomotion
- Train and evaluate RL policies for walking and manipulation

## Concept Overview

Reinforcement learning (RL) enables humanoid robots to learn complex behaviors—walking, running, manipulation—through trial and error in simulation. NVIDIA Isaac Gym provides massively parallel training with thousands of simultaneous environments on a single GPU, dramatically accelerating policy learning. For humanoid robots, RL has produced state-of-the-art locomotion controllers that outperform hand-crafted approaches in robustness and adaptability (Rudin et al., 2022).

## System Architecture

Isaac Gym RL architecture:

- **Vectorized Environments**: Thousands of parallel simulations on GPU
- **PhysX GPU**: Massively parallel articulated body physics
- **Observation Space**: Robot state (joint positions, velocities, IMU)
- **Action Space**: Joint torques or position targets
- **Reward Function**: Shaped signal guiding policy learning
- **Policy Network**: Neural network mapping observations to actions
- **PPO/SAC**: Standard RL algorithms for continuous control

Training occurs entirely on GPU—environments, physics, and policy optimization—enabling billions of simulation steps per day.

## Data Flow and Components

**Training Loop**:
1. Reset all parallel environments to initial states
2. Policy network computes actions from observations
3. Physics engine steps all environments simultaneously
4. Compute rewards based on task objectives
5. Store transitions in replay buffer
6. Update policy using RL algorithm (PPO)
7. Repeat until convergence

**Humanoid Observation Space**:

| Component | Dimensions | Description |
|-----------|-----------|-------------|
| Base linear velocity | 3 | World-frame body velocity |
| Base angular velocity | 3 | IMU gyroscope reading |
| Gravity projection | 3 | Body orientation relative to gravity |
| Joint positions | N_joints | Current joint angles |
| Joint velocities | N_joints | Current joint speeds |
| Previous actions | N_joints | Last commanded actions |
| Command | 3 | Target velocity (vx, vy, ωz) |

## Example Workflow

Training humanoid walking policy:

```python
# Isaac Gym 1.0.x | Python 3.8 | PyTorch 2.0
import torch
from isaacgym import gymapi, gymtorch
from isaacgymenvs.tasks.humanoid import Humanoid
from rl_games.algos_torch import ppo

class HumanoidWalkConfig:
    """Configuration for humanoid walking task."""

    # Environment
    num_envs = 4096  # Parallel environments
    episode_length = 1000

    # Reward weights
    rewards = {
        'tracking_lin_vel': 1.0,    # Match commanded velocity
        'tracking_ang_vel': 0.5,    # Match commanded turning
        'lin_vel_z': -2.0,          # Penalize vertical bouncing
        'ang_vel_xy': -0.05,        # Penalize roll/pitch oscillation
        'orientation': -1.0,         # Keep upright
        'torques': -0.0001,          # Energy efficiency
        'joint_acc': -2.5e-7,        # Smooth motion
        'feet_air_time': 1.0,        # Encourage stepping
        'collision': -1.0,           # Penalize self-collision
        'termination': -200.0,       # Large penalty for falling
    }

    # Termination conditions
    terminate_when_fallen = True
    base_height_threshold = 0.3  # meters

def compute_reward(obs, actions, env_state):
    """Compute shaped reward for locomotion."""
    # Velocity tracking
    lin_vel_error = torch.sum(
        torch.square(obs['command_vel'][:, :2] - obs['base_lin_vel'][:, :2]),
        dim=1
    )
    reward_lin_vel = torch.exp(-lin_vel_error / 0.25)

    # Orientation penalty
    orientation_error = torch.sum(torch.square(obs['gravity_proj'][:, :2]), dim=1)
    reward_orientation = torch.exp(-orientation_error / 0.5)

    # Energy penalty
    reward_torque = torch.sum(torch.square(actions), dim=1)

    total_reward = (
        1.0 * reward_lin_vel +
        0.5 * reward_orientation -
        0.0001 * reward_torque
    )
    return total_reward
```

Training launch:

```bash
# Isaac Gym | CLI training
python train.py task=Humanoid num_envs=4096 max_iterations=5000
```

## Common Failure Modes

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| Reward hacking | Policy finds unintended shortcuts | Refine reward function; add constraints |
| Training instability | Loss spikes, policy collapse | Reduce learning rate; tune PPO hyperparameters |
| Local minima | Policy stuck at suboptimal behavior | Curriculum learning; domain randomization |
| Sim-to-real gap | Policy fails on hardware | See Chapter 3.5 for transfer techniques |

## Summary

Reinforcement learning in Isaac Gym enables training humanoid locomotion policies with unprecedented sample efficiency through massive parallelization. Careful reward shaping guides learning toward stable, efficient gaits. The resulting policies provide the foundation for sim-to-real transfer covered in the next chapter.

**Next**: [Sim-to-Real Transfer](./sim-to-real-transfer)

---

## References

1. Rudin, N., Hoeller, D., Reist, P., & Hutter, M. (2022). Learning to walk in minutes using massively parallel deep reinforcement learning. *Conference on Robot Learning*, 91-100.

2. NVIDIA. (2023). *Isaac Gym documentation*. https://developer.nvidia.com/isaac-gym
