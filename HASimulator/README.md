# HA-VLN Simulator (HASimulator)

<div align="center">
  <img src="../demo/figs/simulator_draft_v2-1.png" alt="HA-VLN Simulator Architecture" width="700"/>
</div>

The **HA-VLN Simulator** extends Habitat-Sim into dynamic environments populated with moving human avatars. It coordinates real-time human activity rendering, multi-threaded timing, dynamic navigation mesh (NavMesh) recalculation, 9-camera multi-view validation, and unified social distance evaluation APIs.

---

## 1. System Architecture

The simulation engine coordinates real-time dynamic human mesh insertion, physics recalculation, egocentric observation rendering, and social compliance metrics:

- **Core Simulation**: Loads Matterport3D architectural scene meshes (`.glb`), manages agent kinematics, and extracts egocentric RGB-D sensor observations.
- **Dynamic Extension Engine**: Animates SMPL human models from the HAPS 2.0 dataset, performs real-time NavMesh dynamic obstacle carving, and handles multi-view human-scene fusion.
- **Perception & Metrics**: Computes social compliance metrics (Collision Rate, Total Collision Rate, distance to humans) and provides optional open-vocabulary object/human detection via GroundingDINO.

---

## 2. Real-Time Human Rendering Engine

Human Rendering is implemented in the class **`HAVLNCE`** of [`environments.py`](environments.py).

### Multi-Threading Execution Model

Human rendering uses child threads for timing and the main thread for inserting / removing human models and recalculating the navigation mesh in real time:
- **Worker Thread**: Manages continuous time tracking, human model frame interpolation (120-frame SMPL mesh sequences), and motion dispatching.
- **Main Thread**: Adds and removes human meshes from the simulator scene graph, queries collision bounds, and synchronizes the agent's physics step.

### Dynamic NavMesh Recomputation & Caching

Because moving humans occupy space, the navigable mesh must reflect dynamic obstacle bounds:
1. On the first episode in a scene, the simulator automatically computes the dynamic navigation mesh accounting for human clearance and saves it to `RECOMPUTE_NAVMESH_PATH` (`../Data/recompute_navmesh`).
2. Subsequent episodes directly load the pre-computed NavMesh cache to maximize simulation throughput.

### Task Configuration Settings

To enable human rendering in your task configuration (e.g., [`config/HAVLNCE_task.yaml`](config/HAVLNCE_task.yaml)):

```yaml
SIMULATOR:
  ADD_HUMAN: True
  HUMAN_GLB_PATH: ../Data/HAPS2_0
  HUMAN_INFO_PATH: ../Data/Multi-Human-Annotations/human_motion.json
  RECOMPUTE_NAVMESH_PATH: ../Data/recompute_navmesh
```

---

## 3. HA-VLN-CE APIs & Measurements

The simulator exposes dedicated APIs for social compliance and human-aware navigation:

| API / Measurement | Category | Description |
|:---|:---|:---|
| **`distance_to_human`** | Social Distance | Computes Euclidean distances and relative angles between the agent and all dynamic humans in the scene ([`measures.py`](measures.py)). |
| **`collisions_detail`** | Safety Measure | Distinguishes physical static obstacle collisions from dynamic human collisions at each navigation step ([`measures.py`](measures.py)). |
| **`human_counting`** | Perception API | Counts the number of visible human subjects in the agent's egocentric observation via GroundingDINO ([`detector.py`](detector.py)). |

### Enabling Measurements in Task Configuration

To record distance and detailed collision events during evaluation, include them in the `MEASUREMENTS` list in [`config/HAVLNCE_task.yaml`](config/HAVLNCE_task.yaml):

```yaml
TASK:
  MEASUREMENTS: [
    DISTANCE_TO_GOAL,
    SUCCESS,
    SPL,
    NDTW,
    PATH_LENGTH,
    ORACLE_SUCCESS,
    STEPS_TAKEN,
    COLLISIONS,
    COLLISIONS_DETAIL,
    DISTANCE_TO_HUMAN
  ]
```

### Enabling Human Counting (Optional Perception Module)

Online human detection and counting relies on GroundingDINO:
1. Set `HUMAN_COUNTING: True` under `SIMULATOR` in [`config/HAVLNCE_task.yaml`](config/HAVLNCE_task.yaml).
2. Install GroundingDINO and download pre-trained weights by following the instructions in [INSTALLATION.md](../INSTALLATION.md#2-native-conda-installation-python-38--cuda-118---recommended).

---

## 4. Benchmark Social & Navigation Metrics (`metric.py`)

The evaluation protocol integrates standard navigation performance with social compliance metrics:

1. **Success Rate (SR, $\uparrow$)**: Proportion of episodes where the agent successfully stops within the goal radius ($d_{\text{stop}} \le 3.0\text{m}$) without human collision:
   $$\text{SR} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(d_i \le 3.0) \cdot \mathbb{I}(e_i = 0)$$
2. **Navigation Error (NE, $\text{m}, \downarrow$)**: Mean geodesic distance between the agent's final stopping position and the goal target:
   $$\text{NE} = \frac{1}{N} \sum_{i=1}^N d_i$$
3. **Collision Rate (CR, $\downarrow$)**: Proportion of human-influenced episodes containing at least one adjusted dynamic human collision:
   $$\text{CR} = \frac{1}{\beta N} \sum_{i=1}^N \min(e_i, 1)$$
4. **Total Collision Rate (TCR, $\downarrow$)**: Average number of human collision events across all episodes:
   $$\text{TCR} = \frac{1}{N} \sum_{i=1}^N e_i$$

---

## 5. Multi-View Human-Scene Fusion (`scripts/human_scene_fusion.py`)

To ensure physical plausibility and eliminate visual artifacts (such as model clipping through furniture or levitation), the framework provides a multi-view annotation verification tool:

- **Setup**: 9 surrounding RGB cameras capture the human model from discrete angles.
- **Camera Configurations**:
  - **8 Side Cameras**: $\theta_{\text{lr}}^i = \frac{\pi i}{8}$ for $i \in \{0, \ldots, 7\}$, with alternating up/down tilt angles.
  - **1 Overhead Camera**: $\theta_{\text{ud}}^9 = \frac{\pi}{2}$ positioned directly above the subject.

To run the multi-view validation capture script:

```bash
cd ../scripts
python3 human_scene_fusion.py
```

Resulting inspection images and videos are written to `scripts/test/` by default.

---

## 6. Task Configuration Presets (`config/`)

The simulator provides 4 standard experimental settings:

| Preset Configuration | Task File | Description |
|:---|:---|:---|
| **HAVLNCE + HAR2R** | [`config/HAVLNCE_task.yaml`](config/HAVLNCE_task.yaml) | Full human-aware continuous environment with HA-R2R socially grounded instructions. |
| **HAVLNCE + R2R** | [`config/HAVLNCE_R2R_task.yaml`](config/HAVLNCE_R2R_task.yaml) | Continuous dynamic human environment with standard R2R-CE instructions. |
| **VLNCE + R2R** | [`config/VLNCE_task.yaml`](config/VLNCE_task.yaml) | Classical static continuous navigation benchmark without humans. |
| **VLNCE + HAR2R** | [`config/VLNCE_HAR2R_task.yaml`](config/VLNCE_HAR2R_task.yaml) | Static environment evaluated on socially enriched instructions. |

To switch presets for training or evaluation, update `BASE_TASK_CONFIG_PATH` in [`agent/config/cma_pm_da_aug_tune.yaml`](../agent/config/cma_pm_da_aug_tune.yaml).