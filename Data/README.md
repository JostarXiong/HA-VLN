# HA-VLN Datasets (Data)

This directory houses the simulation assets, 3D motion models, navigation instructions, and baseline weights for the **HA-VLN 2.0** benchmark.

All dataset episodes, HAPS 2.0 motions, annotations, and pretrained models are officially hosted on Hugging Face:
- 🚀 [**Hugging Face Dataset (fly1113/HA-VLN)**](https://huggingface.co/datasets/fly1113/HA-VLN)

> 💡 *For step-by-step dataset acquisition instructions, refer to the [Installation Guide](../INSTALLATION.md#3-dataset-acquisition).*

---

## 1. Directory Organization

All scene meshes, human activities, and baseline checkpoints reside in `Data/`:

```text
Data/
├── scene_datasets/           # Matterport3D 3D meshes (mp3d/<scan>/<scan>.glb)
├── HAPS2_0/                  # 486 dynamic 3D human motion SMPL models (120 frames each)
├── HA-R2R/                   # Human-aware navigation instructions (train, val_seen, val_unseen)
├── Multi-Human-Annotations/  # Human motion trajectory and placement metadata (human_motion.json)
├── HA-R2R-tools/             # Collision evaluation baselines
├── ddppo-models/             # Pretrained PointGoal ResNet-50 visual depth encoder
└── checkpoints/              # HA-VLN-CMA baseline checkpoints
```

---

## 2. Matterport3D Scene Meshes (`scene_datasets/`)

The physical architectural environments are provided by **Matterport3D**:
- **Terms of Use**: Matterport3D requires signing the official academic Terms of Use form. Request access at the [Matterport3D Project Page](https://niessner.github.io/Matterport/) to receive your personal download script.
- **Download Command**:
  ```bash
  python3 /path/to/download_mp.py -o scene_datasets --task_data habitat
  # After task-data download finishes, press Ctrl-C at the prompt for the main dataset.
  unzip scene_datasets/v1/tasks/mp3d_habitat.zip -d scene_datasets
  ```
- **Expected Layout**: Extracted scenes must reside at:
  ```text
  scene_datasets/mp3d/<scan>/<scan>.glb
  ```

---

## 3. HAPS Dataset 2.0 (Dynamic 3D Human Motions)

In real-world scenarios, human motion dynamically adapts to and interacts with the surrounding region. The **Human Activity and Pose Simulation (HAPS) Dataset 2.0** improves upon [HAPS 1.0](https://github.com/lpercc/HA3D_simulator/) with three core enhancements:
1. **Refined & Diversified Motions**: Covers 172 distinct human activities across indoor and outdoor scene types.
2. **Region-Aware Descriptions**: Identifies **26 distinct regions** across **90 architectural scenes** and generates 486 human activity descriptions, validated through human surveys and quality control.
3. **Motion Diffusion Synthesis**: The [Motion Diffusion Model (MDM)](https://guytevet.github.io/mdm-page/) converts descriptions into **486 detailed 3D human motion models** using the SMPL model, each transformed into a 120-frame motion sequence $\mathcal{H}$.

### Mathematical Formulation

Each **120-frame SMPL mesh sequence** $\mathcal{H} = \langle h_1, h_2, \ldots, h_{120} \rangle$ details 3D human motion and shape parameters. The full motion tensor is parameterized as:

$$\mathbf{H} \in \mathbb{R}^{486 \times 120 \times (10 + 72 + 6890 \times 3)}$$

where:
- $10$ represents the SMPL shape coefficients ($\beta$).
- $72$ represents the pose rotation parameters ($\theta$).
- $6890 \times 3$ represents the 3D coordinates of all mesh vertices per frame.

### Dynamic Motion Sequence Demos

The dataset provides 486 dynamic 3D human motions generated via MDM with natural physical interactions (e.g., walking, searching, conversation, dancing):

| Motion Demo 1 | Motion Demo 2 | Motion Demo 3 |
|:---:|:---:|:---:|
| <img src="../demo/gifs/demo_1.gif" width="230"/> | <img src="../demo/gifs/demo_2.gif" width="230"/> | <img src="../demo/gifs/demo_3.gif" width="230"/> |

| Motion Demo 4 | Motion Demo 5 | Motion Demo 6 |
|:---:|:---:|:---:|
| <img src="../demo/gifs/demo_4.gif" width="230"/> | <img src="../demo/gifs/demo_5.gif" width="230"/> | <img src="../demo/gifs/demo_6.gif" width="230"/> |

---

## 4. HA-R2R Dataset (Human-Aware Room-to-Room)

The **HA-R2R** dataset comprises **16,844 natural language instructions** capturing human activities, crowd encounters, and social navigation requirements.

<div align="center">
  <img src="../demo/figs/human_group_count_vs_length.png" alt="Human Group Count vs Length" width="400"/>
  <img src="../demo/figs/instruction_length_comparison_v2.png" alt="Instruction Length Comparison" width="400"/>
</div>

### Instruction Examples

| # | Instruction Example |
|:---:|:---|
| **1** | Exit the library and turn left. As you proceed straight ahead, you will enter the bedroom, **where you can observe a person actively searching for a lost item, perhaps checking under the bed or inside drawers**. Continue moving forward, **ensuring you do not disturb his search**. As you pass by, **you might see a family engaged in a casual conversation on the porch or terrace**, **be careful not to bump into them**. Maintain your course until you reach the closet. Stop just outside the closet and await further instructions. |
| **2** | Begin your path on the left side of the dining room, **where a group of friends is gathered around a table, enjoying dinner and exchanging stories with laughter**. As you move across this area, **be cautious not to disturb their gathering**. The dining room features a large table and chairs. Proceed through the doorway that leads out of the dining room. Upon entering the hallway, continue straight and then make a left turn. As you walk down this corridor, you might notice framed pictures along the walls. The sound of laughter and conversation from the dining room may still be audible as you move further away. Continue down the hallway until you reach the entrance of the office. Here, **you will observe a person engaged in taking photographs, likely focusing on capturing the view from a window or an interesting aspect of the room**. Stop at this point, ensuring you are positioned at the entrance without obstructing the photographer's activity. |
| **3** | Starting in the living room, **you can observe an individual practicing dance moves, possibly trying out new steps**. As you proceed straight ahead, **you will pass by couches where a couple is engaged in a quiet, intimate conversation, speaking softly to maintain their privacy**. Continue moving forward, ensuring you navigate around any furniture or obstacles in your path. As you transition into the hallway, **notice another couple enjoying a date night at the bar, perhaps sharing drinks and laughter**. **Maintain a steady course without disturbing them**, keeping to the right side of the hallway. Upon reaching the end of your path, you will find yourself back in the living room. Here, **a person is checking their appearance in a hallway mirror, possibly adjusting their attire or hair**. Stop by the right candle mounted on the wall, ensuring you are positioned without blocking any pathways. |
| **4** | Begin by leaving the room and turning to your right. Proceed down the hallway, be careful of any human activity or objects along the way. As you continue, look for the first doorway on your right. Enter through this doorway and advance towards the shelves. Once you reach the vicinity of the shelves, come to a halt and wait there. During this movement, avoid any obstacles or disruptions in the environment. |

*In these examples, bold text highlights human activities, encounters, and agent-human interaction constraints.*

---

## 5. HA-R2R Instruction Generation via Few-Shot Prompting

To generate navigation instructions for HA-R2R, we employ **ChatGPT-4o** and **LLaMA-3-8B-Instruct** to contextually enrich and expand scene information based on the original instructions from R2R-CE.

### Few-Shot Prompting Template

```json
{
  "system": "You are tasked with generating an objective and detailed description of a path and the related scene information based on the given input. Focus solely on observable entities and actions in the scene, avoiding descriptions of smell, atmosphere, or subjective feelings. Ensure clarity and precision in object and human activity descriptions.",
  "examples": "... // Few-shot reference examples",
  "user": "Input:\n[instruction_text]: \"...\";\n[start]: \"...\";\n[during]: \"...\";\n[end]: \"...\";\n\nPlease provide an objective, step-by-step description of the path, focusing on the objects and human activities observed at each stage of the navigation (beginning, during, and end). Expand your description by including character actions, objective descriptions of objects, and details of the movement process. Your description should maintain a neutral tone and avoid embellishments. Please simulate the robot's movement along the path, while incorporating possible connections or interactions between the robot, objects, and human activities.\n\nOutput: ... // generation"
}
```

```json
{
  "example_1": {
    "input": {
      "instruction_text": "Go through the doorway to the hall. Go down the hall past the landing. Take the first door on the right and stop in the doorway.",
      "start": "other room: A person using the room for a quiet phone call.",
      "during": "other room: A person using the room for a quiet phone call.",
      "end": "hallway: An individual cleaning or vacuuming."
    },
    "output": "You should start from the room. Before you walk through the doorway into the hallway, you will notice someone quietly making a phone call, so please remain quiet as you move. Then, proceed down the hallway past the landing. As you continue through the corridor, you will see a responsible cleaner using a vacuum to tidy up. Finally, your destination is at the end of the hallway, enter the first door on the right and stop in the doorway."
  }
}
```

### Iterative Refinement Process

1. **Output Review**: Identify discrepancies, hallucinated objects, or subjective feelings.
2. **Prompt Refinement**: Enforce neutral tone, concrete physical spatial landmarks, and observable human behaviors.
3. **Multi-Round Filtering**: Retain only consistent, physically grounded descriptions aligned with simulator trajectory states.

---

## 6. Human Activities Annotation Pipeline

<div align="center">
  <img src="../demo/figs/dataset_analy.png" alt="Dataset Analysis" width="500"/>
</div>

### Stage 1: Coarse Annotation
- **Goal**: Assign human motions to specific architectural regions $\mathbf{R}$ and scene objects $\mathbf{O}$.
- **Process**: Match motions $h_i$ with objects $j_i$ using semantic embeddings, and optimize placements $\mathbf{p}_{\text{opt}}^{h_i}$ using **Particle Swarm Optimization (PSO)**.
- **Constraints**: Enforce spatial region boundaries and maintain a minimum safe distance $\epsilon = 1.0\text{m}$ from obstacle meshes.

### Stage 2: Fine Annotation
- **Setup**: 9 surrounding RGB cameras capture the human model to eliminate clipping and floating.
- **Camera Angles**: 8 side cameras ($\theta_{\text{lr}}^i = \frac{\pi i}{8}$) with alternating vertical tilt, plus 1 overhead camera ($\theta_{\text{ud}}^9 = \frac{\pi}{2}$).
- **Scale**: 529 human models verified across 374 regions in 90 scenes.

### Multi-Human Interaction & Motion Enrichment
- **Enrichment**: Incorporate coordinated multi-human activities (conversations, walking downstairs, passing by).
- **Manual Quality Control**: 4 rounds of manual verification ensure interaction consistency.
- **Resulting Diversity**: 910 human instances across 428 regions (72 two-human pairs, 59 three-human pairs, 15 four-human groups).
