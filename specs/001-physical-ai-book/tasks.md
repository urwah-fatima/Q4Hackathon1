# Tasks: Physical AI & Humanoid Robotics Technical Book

**Input**: Design documents from `/specs/001-physical-ai-book/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not requested - validation tasks use Docusaurus build and word count checks instead.

**Organization**: Tasks are grouped by user story (module) to enable independent authoring and validation of each module.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1=Module 1, US2=Module 2, US3=Module 3, US4=Module 4)
- Include exact file paths in descriptions

## Path Conventions

- **Content**: `docs/module-N-slug/NN-chapter-slug.md`
- **Module config**: `docs/module-N-slug/_category_.json`
- **References**: `docs/references.md`
- **Introduction**: `docs/intro.md`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize Docusaurus project structure and create module directories

- [x] T001 Create docs/ directory structure per implementation plan
- [x] T002 Create book introduction page in docs/intro.md
- [x] T003 [P] Create Module 1 directory and config in docs/module-1-ros2/_category_.json
- [x] T004 [P] Create Module 2 directory and config in docs/module-2-simulation/_category_.json
- [x] T005 [P] Create Module 3 directory and config in docs/module-3-isaac/_category_.json
- [x] T006 [P] Create Module 4 directory and config in docs/module-4-vla/_category_.json
- [x] T007 Create consolidated references page in docs/references.md

**Checkpoint**: Directory structure ready - chapter authoring can begin

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish citation database and verify MCP documentation availability

**⚠️ CRITICAL**: Chapter authoring should not begin until sources are verified

- [x] T008 Query MCP documentation availability for ROS 2 Humble content
- [x] T009 [P] Verify vendor documentation access for ROS 2 (docs.ros.org)
- [x] T010 [P] Verify vendor documentation access for NVIDIA Isaac (developer.nvidia.com)
- [x] T011 [P] Verify vendor documentation access for Gazebo (gazebosim.org)
- [x] T012 [P] Verify vendor documentation access for Unity ROS (Unity-Technologies/ROS-TCP-Connector)
- [x] T013 Compile initial bibliography with core academic sources (Macenski et al., Quigley et al.)

**Checkpoint**: Foundation ready - all 4 user stories (modules) can begin in parallel

---

## Phase 3: User Story 1 - ROS 2 Fundamentals (Priority: P1) 🎯 MVP

**Goal**: Complete Module 1 covering ROS 2 architecture, communication patterns, Python agents, URDF, and launch files

**Independent Test**: Reader can explain DDS-based pub/sub communication and describe URDF structure for humanoid robots

### Implementation for User Story 1

- [x] T014 [P] [US1] Author Chapter 1.1: ROS 2 Architecture in docs/module-1-ros2/01-ros2-architecture.md
- [x] T015 [P] [US1] Author Chapter 1.2: Nodes, Topics, Services in docs/module-1-ros2/02-nodes-topics-services.md
- [x] T016 [P] [US1] Author Chapter 1.3: Actions & Communication in docs/module-1-ros2/03-actions-communication.md
- [x] T017 [P] [US1] Author Chapter 1.4: Python Agents (rclpy) in docs/module-1-ros2/04-rclpy-python-agents.md
- [x] T018 [P] [US1] Author Chapter 1.5: URDF for Humanoids in docs/module-1-ros2/05-urdf-humanoid-modeling.md
- [x] T019 [P] [US1] Author Chapter 1.6: Launch Files & Parameters in docs/module-1-ros2/06-launch-files-parameters.md
- [x] T020 [US1] Validate Module 1 word counts (each chapter 500-800 words)
- [x] T021 [US1] Validate Module 1 citations (each chapter has at least 1 citation)
- [x] T022 [US1] Run Docusaurus build for Module 1 content

**Checkpoint**: Module 1 complete - readers can learn ROS 2 fundamentals independently

---

## Phase 4: User Story 2 - Digital Twin Simulation (Priority: P2)

**Goal**: Complete Module 2 covering Gazebo setup, physics, URDF/SDF, Unity integration, sensors, and validation

**Independent Test**: Reader can explain simulation validation workflow and identify sim-to-real transfer criteria

### Implementation for User Story 2

- [x] T023 [P] [US2] Author Chapter 2.1: Gazebo Environment Setup in docs/module-2-simulation/01-gazebo-environment-setup.md
- [x] T024 [P] [US2] Author Chapter 2.2: Physics Simulation in docs/module-2-simulation/02-physics-simulation.md
- [x] T025 [P] [US2] Author Chapter 2.3: URDF & SDF Usage in docs/module-2-simulation/03-urdf-sdf-usage.md
- [x] T026 [P] [US2] Author Chapter 2.4: Unity Visualization in docs/module-2-simulation/04-unity-visualization.md
- [x] T027 [P] [US2] Author Chapter 2.5: Sensor Simulation in docs/module-2-simulation/05-sensor-simulation.md
- [x] T028 [P] [US2] Author Chapter 2.6: Validation Strategies in docs/module-2-simulation/06-validation-strategies.md
- [x] T029 [US2] Validate Module 2 word counts (each chapter 500-800 words)
- [x] T030 [US2] Validate Module 2 citations (each chapter has at least 1 citation)
- [x] T031 [US2] Run Docusaurus build for Modules 1-2 content

**Checkpoint**: Modules 1-2 complete - readers can learn ROS 2 and simulation independently

---

## Phase 5: User Story 3 - NVIDIA Isaac Integration (Priority: P3)

**Goal**: Complete Module 3 covering Isaac Sim, synthetic data, Isaac ROS, VSLAM, Nav2, RL, and sim-to-real

**Independent Test**: Reader can explain Isaac ROS perception pipeline and synthetic data training transfer

### Implementation for User Story 3

- [x] T032 [P] [US3] Author Chapter 3.1: Isaac Sim & Synthetic Data in docs/module-3-isaac/01-isaac-sim-synthetic-data.md
- [x] T033 [P] [US3] Author Chapter 3.2: Isaac ROS & VSLAM in docs/module-3-isaac/02-isaac-ros-vslam.md
- [x] T034 [P] [US3] Author Chapter 3.3: Nav2 for Humanoids in docs/module-3-isaac/03-nav2-humanoid-navigation.md
- [x] T035 [P] [US3] Author Chapter 3.4: Reinforcement Learning in docs/module-3-isaac/04-reinforcement-learning.md
- [x] T036 [P] [US3] Author Chapter 3.5: Sim-to-Real Transfer in docs/module-3-isaac/05-sim-to-real-transfer.md
- [x] T037 [P] [US3] Author Chapter 3.6: ROS 2 + Isaac Integration in docs/module-3-isaac/06-ros2-isaac-integration.md
- [x] T038 [US3] Validate Module 3 word counts (each chapter 500-800 words)
- [x] T039 [US3] Validate Module 3 citations (each chapter has at least 1 citation)
- [x] T040 [US3] Run Docusaurus build for Modules 1-3 content

**Checkpoint**: Modules 1-3 complete - readers can learn full simulation-to-deployment pipeline

---

## Phase 6: User Story 4 - Vision-Language-Action Systems (Priority: P4)

**Goal**: Complete Module 4 covering speech-to-command, LLM decomposition, multimodal perception, capstone, edge, and evaluation

**Independent Test**: Reader can explain LLM task decomposition into robot actions and edge deployment constraints

### Implementation for User Story 4

- [x] T041 [P] [US4] Author Chapter 4.1: Speech-to-Command in docs/module-4-vla/01-speech-to-command.md
- [x] T042 [P] [US4] Author Chapter 4.2: LLM Task Decomposition in docs/module-4-vla/02-llm-task-decomposition.md
- [x] T043 [P] [US4] Author Chapter 4.3: Multimodal Perception in docs/module-4-vla/03-multimodal-perception.md
- [x] T044 [P] [US4] Author Chapter 4.4: Capstone Autonomous Humanoid in docs/module-4-vla/04-capstone-autonomous-humanoid.md
- [x] T045 [P] [US4] Author Chapter 4.5: Edge Deployment in docs/module-4-vla/05-edge-deployment.md
- [x] T046 [P] [US4] Author Chapter 4.6: Evaluation & Testing in docs/module-4-vla/06-evaluation-testing.md
- [x] T047 [US4] Validate Module 4 word counts (each chapter 500-800 words)
- [x] T048 [US4] Validate Module 4 citations (each chapter has at least 1 citation)
- [x] T049 [US4] Run Docusaurus build for all Modules 1-4 content

**Checkpoint**: All modules complete - full book content ready

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, cross-references, and deployment preparation

- [x] T050 Consolidate all chapter citations into docs/references.md
- [x] T051 [P] Verify cross-chapter links work (next/previous chapter navigation)
- [x] T052 [P] Verify all acronyms expanded on first use per chapter
- [x] T053 [P] Verify all technical terms defined on first use per chapter
- [x] T054 [P] Verify all code examples have version headers
- [x] T055 Run full Docusaurus production build (npm run build)
- [x] T056 Validate no broken links in build output
- [x] T057 Review capstone chapter (4.4) synthesizes all modules coherently
- [x] T058 Final word count audit across all 24 chapters

**Checkpoint**: Book ready for GitHub Pages deployment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all chapter authoring until sources verified
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - Modules can proceed in parallel (if multiple authors)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
  - Note: Module 4 capstone (T044) benefits from other modules being complete
- **Polish (Phase 7)**: Depends on all modules being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - References Module 1 concepts but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - References Modules 1-2 concepts but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Capstone chapter (T044) ideally authored after other modules for coherence

### Within Each User Story (Module)

All 6 chapters within a module can be authored in parallel (marked [P]):
- Different files, no direct dependencies
- Each chapter is independently completable
- Validation tasks (word count, citations, build) run after all chapters complete

### Parallel Opportunities

- All module directory creation tasks (T003-T006) can run in parallel
- All source verification tasks (T009-T012) can run in parallel
- All 6 chapters within each module can be authored in parallel
- Once Foundational is complete, all 4 modules can be worked on in parallel by different authors

---

## Parallel Example: User Story 1 (Module 1)

```bash
# Launch all 6 chapters for Module 1 together:
Task: "Author Chapter 1.1: ROS 2 Architecture in docs/module-1-ros2/01-ros2-architecture.md"
Task: "Author Chapter 1.2: Nodes, Topics, Services in docs/module-1-ros2/02-nodes-topics-services.md"
Task: "Author Chapter 1.3: Actions & Communication in docs/module-1-ros2/03-actions-communication.md"
Task: "Author Chapter 1.4: Python Agents (rclpy) in docs/module-1-ros2/04-rclpy-python-agents.md"
Task: "Author Chapter 1.5: URDF for Humanoids in docs/module-1-ros2/05-urdf-humanoid-modeling.md"
Task: "Author Chapter 1.6: Launch Files & Parameters in docs/module-1-ros2/06-launch-files-parameters.md"

# Then run validation tasks sequentially:
Task: "Validate Module 1 word counts"
Task: "Validate Module 1 citations"
Task: "Run Docusaurus build for Module 1"
```

---

## Implementation Strategy

### MVP First (User Story 1 / Module 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - verify sources)
3. Complete Phase 3: User Story 1 (Module 1 - ROS 2)
4. **STOP and VALIDATE**: Test Module 1 independently with Docusaurus build
5. Deploy/demo Module 1 if ready

### Incremental Delivery

1. Complete Setup + Foundational → Structure ready
2. Add Module 1 → Validate → Deploy (MVP!)
3. Add Module 2 → Validate → Deploy
4. Add Module 3 → Validate → Deploy
5. Add Module 4 → Validate → Deploy (Full book!)
6. Polish phase → Final deployment

### Parallel Team Strategy

With multiple authors:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Author A: Module 1 (US1)
   - Author B: Module 2 (US2)
   - Author C: Module 3 (US3)
   - Author D: Module 4 (US4)
3. Each module validates independently
4. Final Polish phase brings everything together

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific module (US1=M1, US2=M2, US3=M3, US4=M4)
- Each module should be independently completable and validatable
- Follow section template from contracts/section-schema.md for each chapter
- Follow citation format from contracts/citation-guide.md
- Word count target: 500-800 words per chapter (~750 target)
- Commit after each chapter or logical group
- Stop at any checkpoint to validate module independently
- Avoid: vague tasks, invented APIs, speculative features
