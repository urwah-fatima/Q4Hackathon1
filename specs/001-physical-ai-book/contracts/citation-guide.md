# Citation Guide

**Purpose**: Standardized citation format per Constitution requirements
**Version**: 1.0.0
**Format**: APA 7th Edition

---

## Source Hierarchy (Per Constitution)

Citations MUST follow this priority order:

| Priority | Source Type | When to Use |
|----------|-------------|-------------|
| 1 | MCP-provided documentation | Always primary when available |
| 2 | Official vendor documentation | ROS 2, NVIDIA, Gazebo, Unity official docs |
| 3 | Peer-reviewed publications | IEEE, ACM, arXiv with peer review |
| 4 | Industry whitepapers | NVIDIA technical reports, Open Robotics papers |
| 5 | Technical standards | ISO, IEC, ROS REPs |

**Conflict Resolution**: When sources conflict, cite the higher-priority source as authoritative and note the conflict.

---

## Citation Formats

### 1. MCP Documentation

```
MCP Documentation. (Year). {Document title}. Retrieved from MCP context (accessed YYYY-MM-DD)
```

**Example**:
```
MCP Documentation. (2025). ROS 2 node communication patterns. Retrieved from MCP context (accessed 2025-12-18)
```

**Inline**: (MCP Documentation, 2025)

---

### 2. Vendor Documentation

```
{Organization}. (Year). {Document title}. {URL} (accessed YYYY-MM-DD)
```

**Examples**:

**ROS 2**:
```
Open Robotics. (2023). ROS 2 Humble documentation: Nodes. https://docs.ros.org/en/humble/Concepts/Basic/About-Nodes.html (accessed 2025-12-18)
```

**NVIDIA**:
```
NVIDIA Corporation. (2023). Isaac Sim documentation: Getting started. https://docs.omniverse.nvidia.com/isaacsim/latest/index.html (accessed 2025-12-18)
```

**Gazebo**:
```
Open Robotics. (2023). Gazebo Fortress documentation. https://gazebosim.org/docs/fortress (accessed 2025-12-18)
```

**Unity**:
```
Unity Technologies. (2023). ROS-TCP-Connector documentation. https://github.com/Unity-Technologies/ROS-TCP-Connector (accessed 2025-12-18)
```

**Inline**: (Open Robotics, 2023) or (NVIDIA Corporation, 2023)

---

### 3. Peer-Reviewed Publications

```
{Author, A. A., & Author, B. B.}. (Year). {Article title}. *{Journal/Conference Name}*, {Volume}({Issue}), {Pages}. {DOI or URL}
```

**Examples**:

**Journal Article**:
```
Macenski, S., Foote, T., Gerkey, B., Lalancette, C., & Woodall, W. (2022). Robot Operating System 2: Design, architecture, and uses in the wild. *Science Robotics*, 7(66), eabm6074. https://doi.org/10.1126/scirobotics.abm6074
```

**Conference Paper**:
```
Quigley, M., Conley, K., Gerkey, B., Faust, J., Foote, T., Leibs, J., Wheeler, R., & Ng, A. Y. (2009). ROS: an open-source Robot Operating System. In *ICRA Workshop on Open Source Software* (Vol. 3, No. 3.2, p. 5).
```

**arXiv (with peer review)**:
```
Koenig, N., & Howard, A. (2004). Design and use paradigms for Gazebo, an open-source multi-robot simulator. In *IEEE/RSJ International Conference on Intelligent Robots and Systems* (pp. 2149-2154). https://doi.org/10.1109/IROS.2004.1389727
```

**Inline**: (Macenski et al., 2022) or (Quigley et al., 2009)

---

### 4. Industry Whitepapers

```
{Organization}. (Year). {Title} [White paper]. {URL} (accessed YYYY-MM-DD)
```

**Example**:
```
NVIDIA Corporation. (2022). Isaac Sim: Synthetic data generation for robotics [Technical report]. https://developer.nvidia.com/isaac-sim (accessed 2025-12-18)
```

**Inline**: (NVIDIA Corporation, 2022)

---

### 5. Technical Standards

```
{Organization}. (Year). {Standard number}: {Title}. {URL if available}
```

**Examples**:

**ROS Enhancement Proposals (REPs)**:
```
Open Robotics. (2022). REP-2000: ROS 2 releases and target platforms. https://www.ros.org/reps/rep-2000.html
```

**ISO Standards**:
```
International Organization for Standardization. (2012). ISO 8373:2012 Robots and robotic devices — Vocabulary.
```

**Inline**: (Open Robotics, 2022) or (ISO, 2012)

---

## Code Attribution

For code adapted from external sources:

```python
# Source: https://github.com/ros2/examples/blob/humble/...
# License: Apache 2.0
# Adapted for: [specific modification]
```

**In chapter text**:
```markdown
The following example is adapted from the ROS 2 examples repository (Open Robotics, 2023):
```

---

## Figure Attribution

```markdown
![Alt text](./image.png)
*Figure 1: Description. Source: (Author/Organization, Year). Used with permission / CC BY 4.0 / Public domain.*
```

---

## Inline Citation Placement

**Correct** - citation at end of claim:
```markdown
ROS 2 uses DDS as its middleware layer (Open Robotics, 2023).
```

**Correct** - citation with specific page/section:
```markdown
The QoS policies define reliability and durability (Open Robotics, 2023, Quality of Service section).
```

**Incorrect** - citation before claim:
```markdown
(Open Robotics, 2023) states that ROS 2 uses DDS.
```

---

## References Section Format

Each chapter ends with a References section:

```markdown
## References

1. Macenski, S., Foote, T., Gerkey, B., Lalancette, C., & Woodall, W. (2022). Robot Operating System 2: Design, architecture, and uses in the wild. *Science Robotics*, 7(66), eabm6074.

2. Open Robotics. (2023). ROS 2 Humble documentation. https://docs.ros.org/en/humble/ (accessed 2025-12-18)

3. NVIDIA Corporation. (2023). Isaac Sim documentation. https://docs.omniverse.nvidia.com/isaacsim/latest/ (accessed 2025-12-18)
```

**Ordering**: Alphabetical by first author/organization surname.

---

## Common Citation Errors

| Error | Example | Correction |
|-------|---------|------------|
| Missing access date for URLs | `(Open Robotics, 2023)` | Add `(accessed YYYY-MM-DD)` |
| Inconsistent organization names | `ROS`, `ros.org`, `Open Robotics` | Use `Open Robotics` consistently |
| Missing year | `(NVIDIA)` | Always include year: `(NVIDIA Corporation, 2023)` |
| Non-APA format | `[1]` or `^1` | Use `(Author, Year)` |
| Citing Wikipedia | `(Wikipedia, 2023)` | Find primary source instead |

---

## Checklist

- [ ] Every technical claim has at least one citation
- [ ] All citations use APA 7th edition format
- [ ] URLs include access dates
- [ ] References section is alphabetized
- [ ] Source hierarchy followed (MCP > vendor > academic)
- [ ] Code adaptations attributed with source and license
- [ ] No Wikipedia or unreliable sources
