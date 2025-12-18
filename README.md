# Physical AI & Humanoid Robotics

A comprehensive technical guide covering the complete Physical AI pipeline—from perception to action—using modern robotics frameworks and AI systems.

## Overview

This book provides in-depth coverage of building intelligent humanoid robots, organized into 4 modules with 24 chapters:

### Module 1: ROS 2 Fundamentals
- ROS 2 Architecture (DDS, QoS, middleware)
- Nodes, Topics, and Services
- Actions and Communication
- Python Agents with rclpy
- URDF for Humanoid Modeling
- Launch Files and Parameters

### Module 2: Digital Twin Simulation
- Gazebo Environment Setup
- Physics Simulation
- URDF and SDF Usage
- Unity Visualization
- Sensor Simulation
- Validation Strategies

### Module 3: NVIDIA Isaac Integration
- Isaac Sim and Synthetic Data
- Isaac ROS and VSLAM
- Nav2 for Humanoid Navigation
- Reinforcement Learning
- Sim-to-Real Transfer
- ROS 2 and Isaac Integration

### Module 4: Vision-Language-Action Systems
- Speech-to-Command
- LLM Task Decomposition
- Multimodal Perception
- Capstone: Autonomous Humanoid
- Edge Deployment
- Evaluation and Testing

## Tech Stack

- **Documentation Framework**: [Docusaurus 3.x](https://docusaurus.io/)
- **Robotics Middleware**: ROS 2 Humble Hawksbill
- **Simulation**: Gazebo Fortress, NVIDIA Isaac Sim
- **AI/ML**: PyTorch, TensorRT, Isaac Gym
- **Deployment**: Vercel

## Getting Started

### Prerequisites

- Node.js 18.0 or higher
- npm or yarn

### Installation

```bash
# Clone the repository
git clone https://github.com/urwah-fatima/Q4Hackathon1_p1.git
cd Q4Hackathon1_p1

# Install dependencies
npm install

# Start development server
npm start
```

The site will be available at `http://localhost:3000/`

### Build for Production

```bash
npm run build
```

The static files will be generated in the `build/` directory.

## Project Structure

```
├── docs/                    # Book content (24 chapters)
│   ├── intro.md            # Introduction page
│   ├── module-1-ros2/      # ROS 2 Fundamentals
│   ├── module-2-simulation/ # Digital Twin Simulation
│   ├── module-3-isaac/     # NVIDIA Isaac Integration
│   ├── module-4-vla/       # Vision-Language-Action
│   └── references.md       # Bibliography
├── specs/                   # Spec-driven development artifacts
├── history/                 # Prompt history records
├── src/css/                # Custom styling
├── static/                 # Static assets
├── docusaurus.config.js    # Docusaurus configuration
├── sidebars.js             # Sidebar navigation
└── vercel.json             # Vercel deployment config
```

## Deployment

### Vercel (Recommended)

1. Import the repository in [Vercel Dashboard](https://vercel.com)
2. Vercel auto-detects Docusaurus
3. Click Deploy

### GitHub Pages

```bash
npm run build
npm run deploy
```

## Target Audience

- Advanced students in computer science, robotics, or AI
- Educators developing Physical AI curricula
- Robotics engineers transitioning to humanoid platforms

## Version Targets

| Technology | Version |
|------------|---------|
| ROS 2 | Humble Hawksbill (LTS) |
| Gazebo | Fortress |
| Isaac Sim | 2023.x |
| Python | 3.10+ |
| Docusaurus | 3.x |

## License

This project is for educational purposes.

## Acknowledgments

- [Open Robotics](https://www.openrobotics.org/) - ROS 2 and Gazebo
- [NVIDIA](https://developer.nvidia.com/isaac) - Isaac Sim and Isaac ROS
- [Docusaurus](https://docusaurus.io/) - Documentation framework

---

Built with Docusaurus | Deployed on Vercel
