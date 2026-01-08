# Physical AI & Humanoid Robotics

A comprehensive technical guide covering the complete Physical AI pipeline—from perception to action—using modern robotics frameworks and AI systems.

## Features

- **Interactive AI Chatbot (Pagy)** - Ask questions about the book content in English, Urdu, or Roman Urdu
- **RAG-Powered Search** - Get accurate answers with source references from the book
- **Text Selection Q&A** - Highlight any text and ask "What does this mean?"
- **Mobile Responsive** - Full-screen chat experience on mobile devices
- **Dark/Light Mode** - Seamless theme integration with Docusaurus

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
- **AI Chatbot Backend**: FastAPI + Cohere + Qdrant
- **Embeddings**: Cohere embed-english-v3.0
- **Vector Database**: Qdrant Cloud
- **LLM**: Cohere Command R+
- **Robotics Middleware**: ROS 2 Humble Hawksbill
- **Simulation**: Gazebo Fortress, NVIDIA Isaac Sim
- **AI/ML**: PyTorch, TensorRT, Isaac Gym
- **Deployment**: Vercel (Frontend) + Railway/Render (Backend)

## Getting Started

### Prerequisites

- Node.js 18.0 or higher
- Python 3.11+ (for backend)
- [uv](https://docs.astral.sh/uv/) (Python package manager)

### Frontend Installation

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

### Backend Setup (for AI Chatbot)

```bash
# Navigate to backend
cd backend

# Create .env file with your API keys
cat > .env << EOF
COHERE_API_KEY=your-cohere-api-key
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
EOF

# Install dependencies and run
uv sync
uv run python ingest_markdown.py  # Ingest book content (first time only)
uv run uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000/`

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
├── backend/                 # FastAPI RAG Backend
│   ├── app/                # API application
│   │   ├── main.py        # FastAPI endpoints
│   │   ├── agent.py       # Cohere LLM integration
│   │   ├── retriever.py   # Qdrant vector search
│   │   └── config.py      # Settings
│   └── ingest_markdown.py  # Book content ingestion
├── src/
│   ├── components/
│   │   └── ChatWidget/     # AI Chatbot component
│   ├── theme/
│   │   └── Root.js        # Docusaurus root wrapper
│   └── css/               # Custom styling
├── specs/                   # Spec-driven development artifacts
├── history/                 # Prompt history records
├── static/                 # Static assets
├── docusaurus.config.js    # Docusaurus configuration
├── sidebars.js             # Sidebar navigation
└── vercel.json             # Vercel deployment config
```

## Deployment

### Frontend - Vercel (Recommended)

1. Import the repository in [Vercel Dashboard](https://vercel.com)
2. Vercel auto-detects Docusaurus
3. Click Deploy

### Backend - Railway/Render

1. Create a new project on [Railway](https://railway.app) or [Render](https://render.com)
2. Connect your GitHub repository
3. Set the root directory to `backend`
4. Add environment variables:
   - `COHERE_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
5. Deploy

After deploying the backend, update `src/components/ChatWidget/config.js` with your backend URL.

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
