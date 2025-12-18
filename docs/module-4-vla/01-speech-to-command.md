---
sidebar_position: 1
title: "Speech-to-Command"
description: "Convert natural language voice commands into robot actions using ASR and intent parsing for humanoid control."
keywords: [speech recognition, ASR, voice control, NLP, humanoid, robotics]
---

# Speech-to-Command

**Prerequisites**: Module 3 (NVIDIA Isaac Integration)
**Learning Objectives**: By the end of this chapter, you will be able to:
- Integrate automatic speech recognition (ASR) with ROS 2
- Parse natural language intent into structured robot commands
- Handle ambiguity and confirmation in voice interfaces

## Concept Overview

Speech-to-command enables natural human-robot interaction through voice. For humanoid robots, this capability allows operators to issue high-level instructions ("pick up the cup", "go to the kitchen") without specialized interfaces. The pipeline converts audio to text (ASR), extracts intent and entities (NLU), and maps to executable robot actions. This chapter covers integration patterns for deploying speech interfaces on humanoid systems (Tellex et al., 2020).

## System Architecture

Speech-to-command pipeline:

- **Audio Capture**: Microphone array, noise cancellation, VAD (Voice Activity Detection)
- **ASR Engine**: Whisper, Vosk, or cloud APIs (Google, Azure)
- **Intent Parser**: Rule-based or neural NLU (Rasa, spaCy)
- **Command Mapper**: Intent-to-action translation
- **Confirmation Handler**: Disambiguation, user feedback
- **Action Executor**: ROS 2 action client for robot commands

The pipeline runs as ROS 2 nodes, publishing recognized commands for downstream planning.

## Data Flow and Components

**Speech Processing Flow**:
1. Microphone captures audio stream
2. VAD detects speech segments
3. ASR transcribes speech to text
4. NLU extracts intent and entities
5. Command mapper generates structured command
6. Confirmation requested if ambiguous
7. Action executor sends goal to robot

**Intent Categories for Humanoids**:

| Intent | Example Utterance | Robot Action |
|--------|-------------------|--------------|
| Navigate | "Go to the kitchen" | Nav2 goal |
| Pickup | "Pick up the red cup" | MoveIt grasp |
| Place | "Put it on the table" | MoveIt place |
| Follow | "Follow me" | Person tracking |
| Stop | "Stop" / "Halt" | Emergency stop |

## Example Workflow

Speech-to-command ROS 2 node:

```python
# ROS 2 Humble | Python 3.10 | Whisper + spaCy
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
import whisper
import spacy

class SpeechCommandNode(Node):
    def __init__(self):
        super().__init__('speech_command')

        # Load models
        self.asr = whisper.load_model("base")
        self.nlp = spacy.load("en_core_web_sm")

        # Publishers
        self.cmd_pub = self.create_publisher(String, '/voice_command', 10)
        self.goal_pub = self.create_publisher(PoseStamped, '/goal_pose', 10)

        # Intent patterns
        self.nav_keywords = ['go', 'move', 'navigate', 'walk']
        self.pickup_keywords = ['pick', 'grab', 'get', 'take']

        self.get_logger().info('Speech command node ready')

    def process_audio(self, audio_path):
        # ASR: audio to text
        result = self.asr.transcribe(audio_path)
        text = result['text'].lower().strip()
        self.get_logger().info(f'Transcribed: {text}')

        # NLU: extract intent and entities
        doc = self.nlp(text)
        intent = self.classify_intent(text)
        entities = self.extract_entities(doc)

        # Generate command
        command = {
            'text': text,
            'intent': intent,
            'entities': entities
        }

        self.cmd_pub.publish(String(data=str(command)))
        return command

    def classify_intent(self, text):
        if any(kw in text for kw in self.nav_keywords):
            return 'navigate'
        if any(kw in text for kw in self.pickup_keywords):
            return 'pickup'
        return 'unknown'

    def extract_entities(self, doc):
        entities = {}
        for ent in doc.ents:
            entities[ent.label_] = ent.text
        # Extract locations
        for token in doc:
            if token.dep_ == 'pobj' and token.head.text in ['to', 'in']:
                entities['location'] = token.text
        return entities
```

## Common Failure Modes

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| ASR errors | Misrecognized words | Add domain vocabulary; use noise-robust models |
| Intent confusion | Wrong action selected | Expand training phrases; add confirmation |
| Entity extraction | Missing or wrong targets | Fine-tune NLU; use structured grammars |
| Latency | Slow response to commands | Use streaming ASR; optimize model size |

## Summary

Speech-to-command provides natural interaction with humanoid robots. The ASR-NLU-mapper pipeline converts voice into structured commands for robot execution. Robust systems handle noise, ambiguity, and confirmation to ensure safe, accurate task execution.

**Next**: [LLM Task Decomposition](./llm-task-decomposition)

---

## References

1. Tellex, S., Gopalan, N., Kress-Gazit, H., & Matuszek, C. (2020). Robots that use language. *Annual Review of Control, Robotics, and Autonomous Systems*, 3, 25-55.

2. OpenAI. (2023). *Whisper ASR documentation*. https://github.com/openai/whisper
