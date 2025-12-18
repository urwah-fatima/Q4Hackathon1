/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: ROS 2 Fundamentals',
      items: [
        'module-1-ros2/ros2-architecture',
        'module-1-ros2/nodes-topics-services',
        'module-1-ros2/actions-communication',
        'module-1-ros2/rclpy-python-agents',
        'module-1-ros2/urdf-humanoid-modeling',
        'module-1-ros2/launch-files-parameters',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twin Simulation',
      items: [
        'module-2-simulation/gazebo-environment-setup',
        'module-2-simulation/physics-simulation',
        'module-2-simulation/urdf-sdf-usage',
        'module-2-simulation/unity-visualization',
        'module-2-simulation/sensor-simulation',
        'module-2-simulation/validation-strategies',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: NVIDIA Isaac',
      items: [
        'module-3-isaac/isaac-sim-synthetic-data',
        'module-3-isaac/isaac-ros-vslam',
        'module-3-isaac/nav2-humanoid-navigation',
        'module-3-isaac/reinforcement-learning',
        'module-3-isaac/sim-to-real-transfer',
        'module-3-isaac/ros2-isaac-integration',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action',
      items: [
        'module-4-vla/speech-to-command',
        'module-4-vla/llm-task-decomposition',
        'module-4-vla/multimodal-perception',
        'module-4-vla/capstone-autonomous-humanoid',
        'module-4-vla/edge-deployment',
        'module-4-vla/evaluation-testing',
      ],
    },
    'references',
  ],
};

export default sidebars;
