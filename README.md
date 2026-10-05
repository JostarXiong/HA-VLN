<br>
<p align="center">

<h1 align="center"><strong>HA-VLN 2.0: An Open Benchmark and Leaderboard for Human-Aware Navigation in Discrete and Continuous Environments with Dynamic Multi-Human Interactions</strong></h1>
  <p align="center">
    <span>Yifei Dong<sup>1,*</sup>,</span>
    <span>Fengyi Wu<sup>1,*</sup>,</span>
    <span>Qi He<sup>1</sup>,</span>
    <span>Lingdong Kong<sup>2</sup>,</span>
    <span>Heng Li<sup>1</sup>,</span>
    <span>Minghan Li<sup>1</sup>,</span>
    <span>Zebang Cheng<sup>1</sup>,</span>
    <span>Yuxuan Zhou<sup>1</sup>,</span>
    <span>Jingdong Sun<sup>3</sup>,</span>
    <span>Qi Dai<sup>4</sup>,</span>
    <span>Alexander G. Hauptmann<sup>3</sup>,</span>
    <span>Zhi-Qi Cheng<sup>1,†</sup></span>
    <br>
    <sup>1</sup>UW, <sup>2</sup>NUS, <sup>3</sup>CMU, <sup>4</sup>Microsoft Research<br>
  </p>

<p align="center">
  <a href="https://arxiv.org/abs/2503.14229" target="_blank">
    <img src="https://img.shields.io/badge/arXiv-2503.14229-red">
  </a>
  <a href="https://uwmilab.github.io/HA-VLN-webpage" target="_blank">
    <img src="https://img.shields.io/badge/Webpage-HAVLN-blue">
  </a>
  <a href="https://huggingface.co/datasets/fly1113/HA-VLN" target="_blank">
    <img src="https://img.shields.io/badge/Huggingface-dataset-yellow">
  </a>
  <a href="https://drive.google.com/drive/folders/1WrdsRSPp-xJkImZ3CnI7Ho90lnhzp5GR?usp=sharing" target="_blank">
    <img src="https://img.shields.io/badge/Googledrive-dataset-purple">
  </a>
  <a href="https://github.com/UWMILab/HA-VLN/blob/main/LICENSE" target="_blank">
    <img src="https://img.shields.io/badge/License-MIT-green">
  </a>
</p>

<div align="center">
  <img src="demo/figs/task_define_final-1.png" alt="image" width="750"/>
</div>

## 📰 News

- **[2026-09]** 🏆 We are organizing the [**HA-VLN track**](https://f1y1113.github.io/havln-challenge/) of the [RoboWorld Challenge 2026](https://roboworld2026.github.io/), affiliated with the [RoboPAD Workshop](https://robotpad2026.github.io/) at NeurIPS 2026. Join us in advancing human-aware navigation, participants from all backgrounds are welcome!
- **[2026-06]** 🎉 [HA-VLN 2.0](https://uwmilab.github.io/HA-VLN-webpage) has been accepted to **IROS 2026**!
- **[2025-08]** We have substantially upgraded the repository and improved usability, and organized a small-scale internal competition to support testing and community feedback.
- **[2025-03]** 🚀 We release [HA-VLN 2.0](https://uwmilab.github.io/HA-VLN-webpage), unifying discrete and continuous human-aware navigation with **HAPS 2.0**, dynamic multi-human interactions, and social-awareness evaluation across **16,844 instructions**, check our [Technical Report](https://arxiv.org/abs/2503.14229)!
- **[2024-09]** 🎉 HA-VLN 1.0 has been accepted to the NeurIPS 2024 Datasets and Benchmarks Track!

## 🧭 What does HA-VLN 2.0 look like?

| Navigation Demo 1 | Navigation Demo 2 |
|:---:|:---:|
| <img src="demo/gifs/nav1.gif" width="350"> | <img src="demo/gifs/nav2.gif" width="350"> |
| <details><summary><b>Navigation Instruction:</b> Start by moving forward in the lounge area, <b>where an individual is engaged in a phone conversation while pacing back and forth</b>. Navigate carefully to avoid crossing their path... <i>(Click to expand)</i></summary><br>As you proceed, you will pass by a television mounted on the wall. Continue your movement, <b>observing people relaxing and watching the TV, some seated comfortably on sofas</b>. Further along, <b>notice a group of friends raising their glasses in a toast, enjoying cocktails together</b>. Maintain a steady course, ensuring you do not disrupt their gathering. Finally, reach the end of your path where a potted plant is situated next to a door. Stop at this location, positioning yourself near the plant and door without obstructing access.</details> | <details><summary><b>Navigation Instruction:</b> Exit the room and make a left turn. Proceed down the hallway <b>where an individual is ironing clothes, carefully smoothing out wrinkles on garments</b>. Continue walking and make another left turn... <i>(Click to expand)</i></summary><br>Enter the next room, which is a bedroom. Inside, <b>someone is comfortably seated in bed, engrossed in reading a book</b>. Move past the bed, ensuring not to disturb the reader. Turn left again to enter the bathroom. Once inside, position yourself near the sink and wait there, observing the surroundings without interfering with any activities.</details> |

If you find this repository or our paper useful, please consider **starring** this repository and **citing** our paper. You are also welcome to explore our recent works on world modeling for navigation, including [**LCVN**](https://github.com/UWMILab/LCVN) (**NeurIPS 2026 Oral**), [**UniWM**](https://github.com/F1y1113/UniWM) (**ECCV 2026**), and [**GOViG**](https://github.com/F1y1113/GoViG) (**ACL 2026**).
```bibtex
@inproceedings{dong2026havln,
  author    = {Dong, Yifei and Wu, Fengyi and He, Qi and Kong, Lingdong and Li, Heng and Li, Minghan and Cheng, Zebang and Zhou, Yuxuan and Sun, Jingdong and Dai, Qi and Alexander G. Hauptmann and Cheng, Zhi-Qi},
  title     = {{HA-VLN 2.0: An Open Benchmark and Leaderboard for Human-Aware Navigation in Discrete and Continuous Environments with Dynamic Multi-Human Interactions}},
  booktitle = {2026 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  year      = {2026},
}
```

## Abstract

We present Human-Aware Vision-and-Language Navigation (**HA-VLN**), expanding VLN to include both discrete (**HA-VLN-DE**) and continuous (**HA-VLN-CE**) environments with social behaviors. The [HA-VLN Simulator](HASimulator) enables real-time rendering of human activities and provides unified APIs for navigation development. It introduces the Human Activity and Pose Simulation ([**HAPS 2.0 Dataset**](Data/HAPS2_0)) with detailed 3D human motion models and the HA Room-to-Room ([**HA-R2R**](Data/HA-R2R)) Dataset with complex navigation instructions that include human activities. This repository provides the official implementation, pre-trained weights, and benchmark pipeline for the Cross-Model Attention baseline ([**HA-VLN-CMA**](agent)), addressing visual-language understanding and dynamic decision-making challenges.

## Table of Contents

- [🚀 Quick Start](#-quick-start)
- [🏛️ Framework Architecture](#-framework-architecture)
  - [🖥️ HA-VLN Simulator (`HASimulator/`)](#-ha-vln-simulator-hasimulator)
  - [📊 HAPS 2.0 & HA-R2R Datasets (`Data/`)](#-haps-20--ha-r2r-datasets-data)
  - [🤖 Baseline Agents (`agent/`)](#-baseline-agents-agent)
- [📚 Documentation Guide](#-documentation-guide)
- [Contributing](#contributing) · [Citation](#citation) · [License](#license)

---

## 🚀 Quick Start

In this section, you will download the necessary datasets, set up the Docker environment, reproduce the **HA-VLN-CMA** baseline, and explore the simulator interactively.

### 1. Clone Repository

```bash
git clone https://github.com/UWMILab/HA-VLN.git
cd HA-VLN
```

### 2. Download Datasets & Checkpoint

All scene meshes, human activities, and baseline checkpoints reside in `Data/`:

```bash
# 1. Obtain download_mp.py after Matterport3D access approval:
# https://niessner.github.io/Matterport/
python3 /path/to/download_mp.py -o Data/scene_datasets --task_data habitat
# After task-data download finishes, press Ctrl-C at the prompt for the main dataset.
unzip Data/scene_datasets/v1/tasks/mp3d_habitat.zip -d Data/scene_datasets

# 2. 1-Click download validation episodes, HAPS 2.0, annotations, and CMA weights
python scripts/download_hf.py --destination Data --target all

# 3. Set up the released CMA baseline checkpoint
mkdir -p agent/VLN-CE/data/checkpoints/cma_pm_da_aug_tune
cp Data/checkpoints/HA-VLN-CMA/ckpt.39.pth \
  agent/VLN-CE/data/checkpoints/cma_pm_da_aug_tune/CMA_PM_DA_Aug.pth
```

Matterport3D scene meshes must be obtained separately under its license from [the official dataset page](https://niessner.github.io/Matterport/). Place the extracted scenes at `Data/scene_datasets/mp3d/<scan>/<scan>.glb` before evaluation.

### 3. Reproduce Baseline with Docker

From the repository root, start evaluation on `val_unseen` in one command:

```bash
IMAGE=ghcr.io/jostarxiong/havln-challenge-2026@sha256:78a62cd176d2fd7d0e2825f4cb5be2488ebc5f1a354649b7b4f536a98f1054f4
docker pull "$IMAGE"
DATA_DIR="$(cd Data && pwd -P)"

docker run --gpus all -it --rm \
  --shm-size 16g \
  --mount type=bind,source="$(pwd)",target=/workspace/HA-VLN \
  --mount type=bind,source="$DATA_DIR",target=/workspace/HA-VLN/Data \
  --mount type=bind,source="$DATA_DIR",target=/data/havln2 \
  --workdir /workspace/HA-VLN \
  "$IMAGE" bash -lc 'bash scripts/setup_docker_cma.sh && cd agent &&
    python run.py --exp-config config/cma_pm_da_aug_tune.yaml --run-type eval \
      MODEL.DEPTH_ENCODER.ddppo_checkpoint NONE VIDEO_OPTION "[]"'
```

Results are written to `agent/VLN-CE/data/checkpoints/cma_pm_da_aug_tune/evals/`.
To evaluate `val_seen`, append `EVAL.SPLIT val_seen` to the Python command.

#### Published Benchmark Reference

The following baseline metrics reflect the published HA-VLN 2.0 evaluation results:

| Split | Success Rate (SR) ↑ | Navigation Error (NE, m) ↓ | Collision Rate (CR) ↓ | Total Collision Rate (TCR) ↓ |
|:---|:---:|:---:|:---:|:---:|
| `val_seen` | 0.165 | 6.230 | 0.638 | 13.271 |
| `val_unseen` | 0.114 | 6.502 | 0.689 | 22.352 |

### 4. Interactive Scene Exploration

Experience the human-populated simulator yourself by navigating interactively using the keyboard:

| Key | Action |
|:---:|:---|
| **W** | Move forward ($0.25\text{m}$) |
| **A** | Turn left ($15^{\circ}$) |
| **D** | Turn right ($15^{\circ}$) |

```bash
docker run --gpus all -it --rm \
  --shm-size 16g \
  --mount type=bind,source="$(pwd)",target=/workspace/HA-VLN \
  --mount type=bind,source="$DATA_DIR",target=/workspace/HA-VLN/Data \
  --mount type=bind,source="$DATA_DIR",target=/data/havln2 \
  --workdir /workspace/HA-VLN/scripts \
  "$IMAGE" python demo.py --scan 1LXtFkjw3qL
```

> 💡 *Need a native Conda environment or C++ source build? Check the comprehensive [Environment Installation Guide](INSTALLATION.md).*

---

## 🏛️ Framework Architecture

The HA-VLN 2.0 framework is organized into three core modules:

### 🖥️ HA-VLN Simulator (`HASimulator/`)
Extends Habitat-Sim with dynamic 3D human motion simulation, multi-threaded rendering, and real-time navigation mesh recomputation.
- **Dynamic Human Rendering**: Real-time insertion and animation of dynamic human meshes in class `HAVLNCE`.
- **Social Distance APIs**: Exposes `distance_to_human`, `collisions_detail`, and `human_counting`.
- **Quality Verification**: Multi-view 9-camera human-scene fusion pipeline (`scripts/human_scene_fusion.py`).
- 👉 *Read more in the [Simulator Architecture & API Manual](HASimulator/README.md).*

### 📊 HAPS 2.0 & HA-R2R Datasets (`Data/`)
Provides simulation assets, motion models, and language instructions stored in `Data/`:
- **HAPS 2.0**: 486 dynamic 3D human motion SMPL models across 172 activities and 26 architectural regions.
- **HA-R2R**: 16,844 socially grounded instructions capturing human interactions, crowd encounters, and etiquette.
- **Multi-Human Annotations**: Trajectory metadata (`human_motion.json`) generated via coarse PSO and fine multi-camera tracking.
- 👉 *Read more in the [Datasets & Annotation Pipeline Specification](Data/README.md).*

### 🤖 Baseline Agents (`agent/`)
Provides baseline navigation policies for continuous embodied navigation:
- **HA-VLN-CMA**: Cross-Modal Attention policy integrating RGB-D visual observations, bidirectional GRU language encoding, and goal progress monitoring.
- **Training & Evaluation**: DAgger imitation learning workflows and evaluation harnesses in `agent/VLN-CE/`.
- 👉 *Read more in the [Baseline Agents & Training Manual](agent/README.md).*

---

## 📚 Documentation Guide

For in-depth technical documentation, refer to our dedicated guides:

| Document | Topic & Content |
|:---|:---|
| **[Environment Installation Guide](INSTALLATION.md)** | Docker deployment, Native Conda (Python 3.8 / 3.7), Habitat-Sim C++ build, and GroundingDINO setup. |
| **[Simulator Architecture & APIs](HASimulator/README.md)** | Simulator architecture, real-time human rendering, NavMesh caching, APIs, and task configs. |
| **[Datasets & Annotation Pipeline](Data/README.md)** | HAPS 2.0 SMPL math, HA-R2R dataset details, few-shot prompt templates, and 3-stage annotation. |
| **[Baseline Agents & Training Manual](agent/README.md)** | CMA policy architecture, DAgger imitation training, validation commands, and paper comparison. |

---

## Contributing

We welcome contributions to this project! Please contact yfeidong@uw.edu, fyiwu@uw.edu, or bohanx2@uw.edu.

## Citation

If you find this repository or our paper useful, please consider **starring** this repository and **citing** our paper:

```bibtex
@inproceedings{dong2026havln,
  author    = {Dong, Yifei and Wu, Fengyi and He, Qi and Kong, Lingdong and Li, Heng and Li, Minghan and Cheng, Zebang and Zhou, Yuxuan and Sun, Jingdong and Dai, Qi and Alexander G. Hauptmann and Cheng, Zhi-Qi},
  title     = {{HA-VLN 2.0: An Open Benchmark and Leaderboard for Human-Aware Navigation in Discrete and Continuous Environments with Dynamic Multi-Human Interactions}},
  booktitle = {2026 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  year      = {2026},
}
```

## License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.
