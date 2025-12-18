---
sidebar_position: 2
title: "LLM Task Decomposition"
description: "Use large language models to decompose high-level instructions into executable robot action sequences."
keywords: [LLM, task planning, decomposition, GPT, language models, robotics]
---

# LLM Task Decomposition

**Prerequisites**: Chapter 4.1 (Speech-to-Command)
**Learning Objectives**: By the end of this chapter, you will be able to:
- Integrate LLMs with robot planning systems
- Design prompts for reliable action sequence generation
- Validate and execute LLM-generated plans

## Concept Overview

Large Language Models (LLMs) can decompose complex natural language instructions into sequences of primitive robot actions. When a user says "make me a coffee," the LLM generates steps: navigate to kitchen, locate coffee machine, pick up cup, place under spout, press button, wait, pick up filled cup, deliver. This chapter covers integrating LLMs as high-level planners for humanoid robots, bridging natural language to executable action sequences (Ahn et al., 2022).

## System Architecture

LLM planning architecture:

- **Instruction Input**: Natural language command from user
- **Context Builder**: Assembles scene state, robot capabilities, constraints
- **LLM Engine**: GPT-4, Claude, or local models (Llama)
- **Plan Parser**: Extracts structured actions from LLM output
- **Feasibility Checker**: Validates actions against robot state
- **Executor**: Sequences action calls to ROS 2

The LLM operates as a reasoning module, translating intent into structured plans that downstream systems execute.

## Data Flow and Components

**Planning Pipeline**:
1. Receive high-level instruction
2. Query perception for scene state (objects, locations)
3. Construct prompt with instruction, state, and action primitives
4. LLM generates action sequence
5. Parse output into structured plan
6. Validate each action's preconditions
7. Execute plan, monitoring for failures
8. Replan if execution fails

**Action Primitive Library**:

| Primitive | Parameters | Description |
|-----------|-----------|-------------|
| `navigate(location)` | Room, waypoint | Move to location |
| `pick(object)` | Object ID | Grasp object |
| `place(surface)` | Surface ID | Place held object |
| `open(container)` | Door, drawer | Open articulated object |
| `wait(seconds)` | Duration | Pause execution |
| `speak(message)` | Text | Verbalize to user |

## Example Workflow

LLM-based task planner:

```python
# ROS 2 Humble | Python 3.10 | OpenAI API
import rclpy
from rclpy.node import Node
import openai
import json

class LLMPlanner(Node):
    def __init__(self):
        super().__init__('llm_planner')

        # Available action primitives
        self.primitives = [
            "navigate(location: str)",
            "pick(object_id: str)",
            "place(surface_id: str)",
            "open(container_id: str)",
            "wait(seconds: float)",
            "speak(message: str)"
        ]

        self.system_prompt = """You are a robot task planner. Given a user
instruction and scene state, output a JSON array of actions using only
the available primitives. Each action is {"action": "name", "params": {...}}.
Available primitives: """ + str(self.primitives)

    def plan(self, instruction, scene_state):
        prompt = f"""
Instruction: {instruction}

Scene State:
- Robot location: {scene_state['robot_location']}
- Visible objects: {scene_state['objects']}
- Reachable surfaces: {scene_state['surfaces']}

Generate a plan as a JSON array of actions."""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1  # Low temperature for determinism
        )

        plan_text = response.choices[0].message.content
        plan = self.parse_plan(plan_text)
        return self.validate_plan(plan, scene_state)

    def parse_plan(self, plan_text):
        # Extract JSON from response
        start = plan_text.find('[')
        end = plan_text.rfind(']') + 1
        return json.loads(plan_text[start:end])

    def validate_plan(self, plan, scene_state):
        validated = []
        for action in plan:
            if self.check_preconditions(action, scene_state):
                validated.append(action)
            else:
                self.get_logger().warn(f'Invalid action: {action}')
                break
        return validated

    def check_preconditions(self, action, state):
        # Verify action is feasible given current state
        if action['action'] == 'pick':
            return action['params']['object_id'] in state['objects']
        return True  # Default: assume valid
```

Example interaction:

```python
# Example usage
scene = {
    'robot_location': 'living_room',
    'objects': ['cup_01', 'book_02', 'remote_03'],
    'surfaces': ['coffee_table', 'shelf']
}

plan = planner.plan("Bring me the cup from the living room", scene)
# Output: [
#   {"action": "navigate", "params": {"location": "coffee_table"}},
#   {"action": "pick", "params": {"object_id": "cup_01"}},
#   {"action": "navigate", "params": {"location": "user"}},
#   {"action": "speak", "params": {"message": "Here is your cup"}}
# ]
```

## Common Failure Modes

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| Hallucinated actions | Non-existent primitives | Constrain output format; validate actions |
| Infeasible plans | Actions with unmet preconditions | Include state in prompt; add feasibility check |
| Missing steps | Plan skips necessary actions | Improve prompt; few-shot examples |
| Inconsistent output | Variable JSON format | Structured output parsing; retry logic |

## Summary

LLMs enable humanoid robots to understand complex instructions and generate executable plans. Careful prompt engineering, output parsing, and feasibility validation ensure reliable plan generation. This capability bridges natural language interaction to robot execution, forming the cognitive layer of Physical AI systems.

**Next**: [Multimodal Perception](./multimodal-perception)

---

## References

1. Ahn, M., et al. (2022). Do as I can, not as I say: Grounding language in robotic affordances. *Conference on Robot Learning*.

2. Brohan, A., et al. (2023). RT-2: Vision-Language-Action models transfer web knowledge to robotic control. *arXiv preprint*.
