<br>
<p align="center">

<h1 align="center"><strong>HA-VLN 2.0: An Open Benchmark and Leaderboard for Human-Aware Navigation in Discrete and Continuous Environments with Dynamic Multi-Human Interactions</strong></h1>
  <p align="center"><span><a href=""></a></span>
              <a>Yifei Dong<sup>1,*</sup>,</a>
              <a>Fengyi Wu<sup>1,*</sup>,</a>
              <a>Qi He<sup>1</sup>,</a>
              <a>Lingdong Kong<sup>2</sup>,</a>
              <a>Heng Li<sup>1</sup>,</a>
              <a>Minghan Li<sup>1</sup>,</a>
              <a>Zebang Cheng<sup>1</sup>,</a>
              <a>Yuxuan Zhou<sup>1</sup>,</a>
              <a>Jingdong Sun<sup>3</sup>,</a>
              <a>Qi Dai<sup>4</sup>,</a>
              <a>Alexander G. Hauptmann<sup>3</sup>,</a>
              <a>Zhi-Qi Cheng<sup>1,†</sup></a>
    <br>
    <sup>1</sup>UW, <sup>2</sup>NUS, <sup>3</sup>CMU, <sup>4</sup>Microsoft Research<br>
  </p>

<p align="center">
  <a href="https://arxiv.org/abs/2503.14229" target="_blank">
    <img src="https://img.shields.io/badge/arXiv-2503.14229-red">
  </a>
  <a href="https://ha-vln-project.vercel.app/" target="_blank">
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
  <img src="demo/figs/task_define_final-1.png" alt="image" width="700"/>
</div>

## 🧭 What does HA-VLN 2.0 look like?

Navigation Demo 1|Navigation Demo 2
--|--
<img src="demo/gifs/nav1.gif" width="350">|<img src="demo/gifs/nav2.gif" width="350">
**Navigation Instruction**: Start by moving forward in the lounge area, **where an individual is engaged in a phone conversation while pacing back and forth**. Navigate carefully to avoid crossing their path. As you proceed, you will pass by a television mounted on the wall. Continue your movement, **observing people relaxing and watching the TV, some seated comfortably on sofas**. Further along, **notice a group of friends raising their glasses in a toast, enjoying cocktails together**. Maintain a steady course, ensuring you do not disrupt their gathering. Finally, reach the end of your path where a potted plant is situated next to a door. Stop at this location, positioning yourself near the plant and door without obstructing access.|**Navigation Instruction**: Exit the room and make a left turn. Proceed down the hallway **where an individual is ironing clothes, carefully smoothing out wrinkles on garments**. Continue walking and make another left turn. Enter the next room, which is a bedroom. Inside, **someone is comfortably seated in bed, engrossed in reading a book**. Move past the bed, ensuring not to disturb the reader. Turn left again to enter the bathroom. Once inside, position yourself near the sink and wait there, observing the surroundings without interfering with any activities.

If you find this repository or our paper useful, please consider **starring** this repository and **citing** our paper. You are also welcome to explore our other recent works towards world modeling in navigation, including [**UniWM**](https://github.com/F1y1113/UniWM) and [**GOViG**](https://github.com/F1y1113/GoViG),
```bibtex
@misc{dong2025havln20openbenchmark,
      title={HA-VLN 2.0: An Open Benchmark and Leaderboard for Human-Aware Navigation in Discrete and Continuous Environments with Dynamic Multi-Human Interactions}, 
      author={Yifei Dong and Fengyi Wu and Qi He and Zhi-Qi Cheng and Heng Li and Minghan Li and Zebang Cheng and Yuxuan Zhou and Jingdong Sun and Qi Dai and Alexander G Hauptmann},
      year={2025},
      eprint={2503.14229},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2503.14229}, 
}
```

## Abstract

We present Human-Aware Vision-and-Language Navigation (**HA-VLN**), expanding VLN to include both discrete (**HA-VLN-DE**) and continuous (**HA-VLN-CE**) environments with social behaviors. The [HA-VLN Simulator](HASimulator) enables real-time rendering of human activities and provides unified APIs for navigation development. It introduces the Human Activity and Pose Simulation ([**HAPS 2.0 Dataset**](Data/HAPS2_0)) with detailed 3D human motion models and the HA Room-to-Room ([**HA-R2R**](Data/HA-R2R)) Dataset with complex navigation instructions that include human activities. We propose an HA-VLN Vision-and-Language model ([**HA-VLN-VL**](agent)) and a Cross-Model Attention model ([**HA-VLN-CMA**](agent)) to address visual-language understanding and dynamic decision-making challenges.

## Table of Contents

- [🚀 Quick Start](#-quick-start)
- [🎮 HA-VLN Simulator (HASimulator)](#-ha-vln-simulator-hasimulator)
- [📊 HAPS 2.0 & HA-R2R Datasets (Data)](#-haps-20--ha-r2r-datasets-data)
- [🤖 HA-VLN-CMA Baseline Agent (agent)](#-ha-vln-cma-baseline-agent-agent)
- [Contributing](#contributing) · [Citation](#citation) · [License](#license)

---

## 🚀 Quick Start

In this section, you will download the necessary datasets and deploy the essential environment within Docker. Then, you can reproduce our proposed HA-VLN-CMA baseline model and observe its benchmark performance. Detailed documentation for simulator usage, agent training, and dataset details is provided in the following sections.

### 1. Clone Repository

```bash
git clone https://github.com/UWMILab/HA-VLN.git
cd HA-VLN
```

### 2. Download Datasets

All scene meshes, human activities, and baseline checkpoints reside in `Data/`:

```bash
# 1. Download Matterport3D scene meshes into Data/scene_datasets
# License required: https://niessner.github.io/Matterport/
python2 download_mp.py -o Data/scene_datasets --type matterport_mesh house_segmentations region_segmentations poisson_meshes

# 2. 1-Click download HA-R2R, HAPS 2.0, annotations, and pretrained models from Hugging Face
pip install huggingface-hub
huggingface-cli download fly1113/HA-VLN --local-dir Data --repo-type dataset

# 3. Set up the released CMA baseline checkpoint
mkdir -p agent/VLN-CE/data/checkpoints/cma_pm_da_aug_tune
cp Data/checkpoints/HA-VLN-CMA/ckpt.39.pth agent/VLN-CE/data/checkpoints/cma_pm_da_aug_tune/CMA_PM_DA_Aug.pth
```

### 3. Reproduce Baseline with Docker

Pull our pre-built Docker image and run evaluation on `val_unseen` in one command:

```bash
IMAGE=ghcr.io/jostarxiong/havln-challenge-2026@sha256:78a62cd176d2fd7d0e2825f4cb5be2488ebc5f1a354649b7b4f536a98f1054f4
docker pull "$IMAGE"

docker run --gpus all -it --rm \
  --shm-size 16g \
  --mount type=bind,source="$(pwd)",target=/workspace/HA-VLN \
  --mount type=bind,source="$(pwd)/Data",target=/workspace/HA-VLN/Data \
  --mount type=bind,source="$(pwd)/Data",target=/data/havln2 \
  --workdir /workspace/HA-VLN/agent \
  "$IMAGE" python run.py --exp-config config/cma_pm_da_aug_tune.yaml --run-type eval
```

*(Tip: To launch an interactive development shell, simply change `python run.py ...` to `bash`)*.

#### Expected Benchmark Validation Results

| Split | Score | SR | NE | CR | TCR |
|:---|:---:|:---:|:---:|:---:|:---:|
| `val_seen` | 15.47 | 0.165 | 6.230 | 0.638 | 13.271 |
| `val_unseen` | 11.94 | 0.114 | 6.502 | 0.689 | 22.352 |

---

## 🎮 HA-VLN Simulator (HASimulator)

The **HA-VLN Simulator** extends Habitat-Sim with dynamic 3D human motion simulation, real-time navigation mesh recomputation, multi-view human-scene fusion, social distance measurements, and interactive navigation tools.

> 👉 *For complete simulator architecture diagrams, task configuration presets, and internal APIs, see [HASimulator/README.md](HASimulator/).*

### 1. Real-time Human Rendering

Human Rendering is defined in the class **HAVLNCE** of [HASimulator/environments.py](HASimulator/environments.py).

Human Rendering uses child threads for timing and the main thread for adding / removing human models and recalculating the required navmesh in real time.

In the first use, the navmesh will be automatically calculated and saved to support operations such as collision calculation, and the subsequent use will directly load the previously generated navmesh. To enable human rendering, modify the following settings in [HAVLN-CE task config](HASimulator/config/HAVLNCE_task.yaml):

```yaml
SIMULATOR:
  ADD_HUMAN: True
  HUMAN_GLB_PATH: ../Data/HAPS2_0
  HUMAN_INFO_PATH: ../Data/Multi-Human-Annotations/human_motion.json
  RECOMPUTE_NAVMESH_PATH: ../Data/recompute_navmesh
```

---

### 2. Human-Scene Fusion (Multi-View Rendering)

To detect visual anomalies (such as floating meshes or model clipping) and verify human alignment within photorealistic scenes, the simulator provides a multi-view human-scene fusion rendering pipeline in [scripts/human_scene_fusion.py](scripts/human_scene_fusion.py).

To reproduce the [**Multi-view human annotation videos**](https://drive.google.com/drive/folders/1XvGHgLJ0MFDNY_k_iVwE_oGpfBfBaZif?usp=sharing), run the fusion rendering script:
```bash
cd scripts
python3 human_scene_fusion.py
```
*(Rendered frames are output to `scripts/test/` by default. You can modify `output_path` inside [scripts/human_scene_fusion.py](scripts/human_scene_fusion.py)).*

---

### 3. Simulator APIs & Social Measurements

As detailed in Section 4 of the HA-VLN 2.0 paper, the simulator exposes unified APIs and evaluation measures in [HASimulator/measures.py](HASimulator/measures.py) and [HASimulator/metric.py](HASimulator/metric.py) to assess agent behavior and personal-space compliance:

- **`distance_to_human`**: Computes the exact Euclidean distance and relative angle between the agent and all dynamic humans in the scene at each timestep.
- **`collisions_detail`**: Tracks per-step collisions with environment obstacles and humans, distinguishing physical collisions from social-distance infractions.
- **`human_counting`**: Detects and counts visible individuals within the agent's current egocentric observation using an open-set perception detector ([HASimulator/detector.py](HASimulator/detector.py)).
- **Social Evaluation Metrics**: Implements benchmark evaluation metrics in [HASimulator/metric.py](HASimulator/metric.py), including **Total Collision Rate (TCR)**, **Collision Rate (CR)**, **Success Rate (SR)**, and **Navigation Error (NE)**.

Enable social distance measurements under `TASK.MEASUREMENTS` and `SIMULATOR.HUMAN_COUNTING` in [HASimulator/config/HAVLNCE_task.yaml](HASimulator/config/HAVLNCE_task.yaml) (see [HASimulator/README.md](HASimulator/) for complete measurement lists and all 4 task configuration presets).

<details>
<summary><b>Setup GroundingDINO for Human Counting (Optional)</b></summary>
<br>

*Note: GroundingDINO is an optional simulator perception module for online human detection, observation logging, and reward shaping. Standard navigation policies (such as HA-VLN-CMA) do not require GroundingDINO.*

If you wish to enable the real-time human detection and counting module:

```bash
cd "$HA_VLN_ROOT"
conda install -c nvidia/label/cuda-11.8.0 -c conda-forge \
  cuda-toolkit gcc_linux-64=11 gxx_linux-64=11 sysroot_linux-64=2.17 -y
export CUDA_HOME="$CONDA_PREFIX"
export CC="$CONDA_PREFIX/bin/x86_64-conda-linux-gnu-gcc"
export CXX="$CONDA_PREFIX/bin/x86_64-conda-linux-gnu-g++"

git clone https://github.com/IDEA-Research/GroundingDINO.git HASimulator/GroundingDINO
git -C HASimulator/GroundingDINO checkout df5b48a3efbaa64288d8d0ad09b748ac86f22671
MAX_JOBS=2 python -m pip install --no-deps --no-build-isolation \
  -e HASimulator/GroundingDINO

mkdir -p HASimulator/GroundingDINO/weights
curl -fL --retry 3 \
  https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth \
  -o HASimulator/GroundingDINO/weights/groundingdino_swint_ogc.pth
python -m pip check
```

</details>

---

### 4. Interactive Scene Exploration

You can navigate through a scene interactively using the keyboard:
| Key | Action        |
|:----|:--------------|
| **W** | Move forward |
| **A** | Turn left    |
| **D** | Turn right   |

```bash
cd scripts
python demo.py --scan 1LXtFkjw3qL
```
You may change the scan id to that of the scene you want to explore.

---

### 5. Simulator Installation

The HA-VLN Simulator relies on Habitat-Sim 0.1.7 with headless EGL rendering support. We provide both a pre-built Docker image (recommended for zero-configuration deployment) and native Conda setup instructions.

#### Option A: Docker Environment (Recommended)

Our Docker image pre-configures CUDA 11.8, PyTorch 2.0.1, Habitat-Sim 0.1.7, Habitat-Lab 0.1.7, and headless graphics drivers (`libEGL`, `libGLX`), enabling out-of-the-box execution across Linux and WSL2 without dependency conflicts.

1. **Pull the Docker image**:
   ```bash
   IMAGE=ghcr.io/jostarxiong/havln-challenge-2026@sha256:78a62cd176d2fd7d0e2825f4cb5be2488ebc5f1a354649b7b4f536a98f1054f4
   docker pull "$IMAGE"
   ```

2. **Launch an interactive shell in the container**:
   ```bash
   docker run --gpus all -it --rm \
     --shm-size 16g \
     --mount type=bind,source="$(pwd)",target=/workspace/HA-VLN \
     --mount type=bind,source="$(pwd)/Data",target=/workspace/HA-VLN/Data \
     --mount type=bind,source="$(pwd)/Data",target=/data/havln2 \
     --workdir /workspace/HA-VLN \
     "$IMAGE" bash
   ```

3. **Run Simulator scripts inside Docker**:
   You can run simulator pipelines directly inside the interactive container, or pass the command directly:
   ```bash
   # Multi-view Human-Scene Fusion rendering
   docker run --gpus all -it --rm \
     --shm-size 16g \
     --mount type=bind,source="$(pwd)",target=/workspace/HA-VLN \
     --mount type=bind,source="$(pwd)/Data",target=/workspace/HA-VLN/Data \
     --mount type=bind,source="$(pwd)/Data",target=/data/havln2 \
     --workdir /workspace/HA-VLN/scripts \
     "$IMAGE" python human_scene_fusion.py

   # Interactive keyboard exploration (requires display/X11 forwarding if GUI attached)
   docker run --gpus all -it --rm \
     --shm-size 16g \
     --mount type=bind,source="$(pwd)",target=/workspace/HA-VLN \
     --mount type=bind,source="$(pwd)/Data",target=/workspace/HA-VLN/Data \
     --mount type=bind,source="$(pwd)/Data",target=/data/havln2 \
     --workdir /workspace/HA-VLN/scripts \
     "$IMAGE" python demo.py --scan 1LXtFkjw3qL
   ```

> **Key Docker Flags**:
> - `--gpus all`: Grants container access to host GPUs for headless EGL rendering.
> - `--shm-size 16g`: Allocates shared memory for PyTorch dataloading and multi-threading.
> - `--mount type=bind,...`: Dual-mounts host `Data/` to both `/workspace/HA-VLN/Data` and `/data/havln2`, satisfying both legacy and current config paths without manual edits.

#### Option B: Native Installation (Optional)

<details>
<summary><b>Native Simulator Setup (Python 3.8 / CUDA 11.8)</b></summary>
<br>

The following Linux setup uses Python 3.8 and CUDA 11.8. Keep Habitat-Sim and Habitat-Lab at **0.1.7**:

```bash
HA_VLN_ROOT="$(pwd)"
conda create -n havlnce python=3.8 pip=24.0 -c conda-forge -y
conda activate havlnce
conda install -c aihabitat -c conda-forge \
  "habitat-sim=0.1.7=*headless*" "numpy=1.23.5" \
  python-lmdb libxcrypt libopengl libglx -y

python -m pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 \
  --index-url https://download.pytorch.org/whl/cu118

git clone --branch v0.1.7 --depth 1 \
  https://github.com/facebookresearch/habitat-lab.git habitat-lab
python -m pip install -c requirements-py38.txt \
  -r habitat-lab/requirements.txt setuptools pytest-runner \
  tensorboard moviepy webdataset ifcfg msgpack_numpy
python -m pip install --no-deps --no-build-isolation -e habitat-lab

export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:${LD_LIBRARY_PATH:-}"
export DISPLAY=""
export EGL_DEVICE_ID=0
```

<details>
<summary>Alternative: build Habitat-Sim 0.1.7 from source</summary>

Use this instead of the pre-built package if modifying C++ simulator source:
```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
  cmake build-essential libjpeg-dev libglm-dev libgl1 \
  libegl1-mesa-dev mesa-utils xorg-dev freeglut3-dev
git clone --branch v0.1.7 --recursive \
  https://github.com/facebookresearch/habitat-sim.git habitat-sim
cd habitat-sim
python -m pip install -r requirements.txt -c "$HA_VLN_ROOT/requirements-py38.txt"
python setup.py install --headless
cd "$HA_VLN_ROOT"
```
</details>

<details>
<summary>Legacy Python 3.7 Environment (Historical Reference)</summary>

These commands retain the original software stack for historical reference. Please install `habitat-lab` (v0.1.7) and `habitat-sim` (v0.1.7) following [ETPNav](https://github.com/MarSaKi/ETPNav/) (note that this uses `python==3.7`):
```bash
conda create -n havlnce python=3.7
conda activate havlnce
conda install -c aihabitat -c conda-forge habitat-sim=0.1.7 headless
git clone --branch v0.1.7 https://github.com/facebookresearch/habitat-lab.git
cd habitat-lab
pip install -r requirements.txt
pip install -r habitat_baselines/rl/requirements.txt
python setup.py develop --all
cd $(git rev-parse --show-toplevel)
```
</details>

</details>

---

## 📊 HAPS 2.0 & HA-R2R Datasets (Data)

Simulation environments in HA-VLN combine Matterport3D architecture meshes with HAPS 2.0 dynamic human motions and HA-R2R navigation instructions.

### 1. Dataset Organization

All simulation environments, meshes, human motions, and sensor models reside in the `Data/` directory:

```text
Data/
├── scene_datasets/           # Matterport3D 3D meshes & segmentations
├── HAPS2_0/                  # 486 dynamic 3D human motion SMPL models (120 frames each)
├── HA-R2R/                   # Human-aware navigation instructions (train, val_seen, val_unseen)
├── Multi-Human-Annotations/  # Human motion trajectory and placement metadata (human_motion.json)
└── ddppo-models/             # Pretrained PointGoal ResNet-50 visual depth encoder
```

### 2. Dataset Download & Breakdown

All HA-VLN simulation assets, motion models, annotations, and observation backbones are hosted on Hugging Face at [**fly1113/HA-VLN**](https://huggingface.co/datasets/fly1113/HA-VLN), while the underlying architectural 3D meshes are provided by **Matterport3D**.

#### 1. Matterport3D Scene Meshes (`Data/scene_datasets`)
- **License & Access**: Matterport3D requires signing the official academic Terms of Use. Request access at the [Matterport3D Project Page](https://niessner.github.io/Matterport/) to receive your personal download script and authentication token.
- **Download Command**:
  ```bash
  python2 download_mp.py -o Data/scene_datasets --type matterport_mesh house_segmentations region_segmentations poisson_meshes
  ```

#### 2. HA-VLN Simulation Assets (`fly1113/HA-VLN` on Hugging Face)

Download individual components based on your research needs:

```bash
pip install huggingface-hub

# 1. HA-R2R navigation episodes
huggingface-cli download fly1113/HA-VLN --include "HA-R2R/*" --local-dir Data --repo-type dataset

# 2. HAPS 2.0 3D dynamic human motions
huggingface-cli download fly1113/HA-VLN --include "HAPS2_0/*" --local-dir Data --repo-type dataset

# 3. Multi-human motion & placement annotations (human_motion.json)
huggingface-cli download fly1113/HA-VLN --include "Multi-Human-Annotations/*" --local-dir Data --repo-type dataset

# 4. Pretrained PointGoal ResNet-50 visual depth observation backbone
huggingface-cli download fly1113/HA-VLN --include "ddppo-models/*" --local-dir Data --repo-type dataset
```

<details>
<summary><b>Alternative: Download via Script & Standalone Links (Google Drive)</b></summary>
<br>

- **HA-R2R & HAPS 2.0 via Google Drive** (`gdown` required):
  ```bash
  bash scripts/download_data.sh
  ```
- **Pretrained Depth Encoder Weights (Direct Link)**:
  Download from [ddppo-models.zip](https://dl.fbaipublicfiles.com/habitat/data/baselines/v1/ddppo/ddppo-models.zip) and extract contents to `Data/ddppo-models/{model}.pth`.

</details>

### 3. HAPS Dataset 2.0 (3D Human Motion Models)

In real-world scenarios, human motion typically adapts and interacts with the surrounding region. The proposed **Human Activity and Pose Simulation (HAPS) Dataset 2.0** improves upon [**HAPS 1.0**](https://github.com/lpercc/HA3D_simulator/) by making the following enhancements:  
1. *Refining and diversifying human motions.*  
2. *Providing descriptions closely tied to region awareness.*   

HAPS 2.0 mitigates the limitations of existing human motion datasets by identifying **26 distinct regions** across **90 architectural scenes** and generating **486 human activity descriptions**, encompassing both **indoor and outdoor environments**. These descriptions, validated through **human surveys** and **quality control using ChatGPT-4**, include realistic actions and region annotations (e.g., *"workout gym exercise: An individual running on a treadmill"*).

The [**Motion Diffusion Model (MDM)**](https://guytevet.github.io/mdm-page/) converts these descriptions into **486 detailed 3D human motion models** $\mathbf{H}$[^1] using the **SMPL model**, each transformed into a **120-frame motion sequence** $\mathcal{H}$.  

Each **120-frame SMPL mesh sequence** $\mathcal{H} = \langle h_1, h_2, \ldots, h_{120} \rangle$ details **3D human motion and shape information** through the **SMPL model**.

<div align="center">
  <img src="demo/gifs/havln.gif" alt="image2" width="700"/>
</div>

**Overall View of Nine Annotated Scenarios from HA-VLN Simulator (90 scans in total)** 

<div align="center">
  <img src="demo/figs/overview_example-1.png" alt="image2" width="700"/>
</div>

**Single Humans with Movements (910 Humans in total)** 

Demo 1|Demo 2|Demo 3
--|--|--
<img src="demo/gifs/demo_1.gif" width="280">|<img src="demo/gifs/demo_2.gif" width="280">|<img src="demo/gifs/demo_3.gif" width="280">

Demo 4|Demo 5|Demo 6
--|--|--
<img src="demo/gifs/demo_4.gif" width="280">|<img src="demo/gifs/demo_5.gif" width="280">|<img src="demo/gifs/demo_6.gif" width="280">

[^1]: **H** = **R**<sup>486 × 120 × (10 + 72 + 6890 × 3)</sup>, representing **486 models**, each with **120 frames**, including **shape, pose, and mesh vertex parameters**.

### 4. HA-R2R Dataset (Navigation Instructions)

Instruction Examples Table presents four instruction examples from the **Human-Aware Room-to-Room (HA-R2R) dataset**. These cases include various scenarios such as:
- **Multi-human interactions** (e.g., 1, 2, 3)
- **Agent-human interactions** (e.g., 1, 2, 3)
- **Agent encounters four or more humans** (e.g., 3)
- **No humans encountered** (e.g., 4)

These examples illustrate the diversity of **human-aligned navigation instructions** that challenge the agent in our task.

<div align="center">
  <img src="demo/figs/human_group_count_vs_length.png" alt="image" width="400"/>
  <img src="demo/figs/instruction_length_comparison_v2.png" alt="image" width="400"/>
</div>

#### Instruction Examples Table

| **Instruction Example** |
|:-------------------------|
| **1.** Exit the library and turn left. As you proceed straight ahead, you will enter the bedroom, **where you can observe a person actively searching for a lost item, perhaps checking under the bed or inside drawers**. Continue moving forward, **ensuring you do not disturb his search**. As you pass by, **you might see a family engaged in a casual conversation on the porch or terrace**, **be careful not to bump into them**. Maintain your course until you reach the closet. Stop just outside the closet and await further instructions. |
| **2.** Begin your path on the left side of the dining room, **where a group of friends is gathered around a table, enjoying dinner and exchanging stories with laughter**. As you move across this area, **be cautious not to disturb their gathering**. The dining room features a large table and chairs. Proceed through the doorway that leads out of the dining room. Upon entering the hallway, continue straight and then make a left turn. As you walk down this corridor, you might notice framed pictures along the walls. The sound of laughter and conversation from the dining room may still be audible as you move further away. Continue down the hallway until you reach the entrance of the office. Here, **you will observe a person engaged in taking photographs, likely focusing on capturing the view from a window or an interesting aspect of the room**. Stop at this point, ensuring you are positioned at the entrance without obstructing the photographer's activity. |
| **3.** Starting in the living room, **you can observe an individual practicing dance moves, possibly trying out new steps**. As you proceed straight ahead, **you will pass by couches where a couple is engaged in a quiet, intimate conversation, speaking softly to maintain their privacy**. Continue moving forward, ensuring you navigate around any furniture or obstacles in your path. As you transition into the hallway, **notice another couple enjoying a date night at the bar, perhaps sharing drinks and laughter**. **Maintain a steady course without disturbing them**, keeping to the right side of the hallway. Upon reaching the end of your path, you will find yourself back in the living room. Here, **a person is checking their appearance in a hallway mirror, possibly adjusting their attire or hair**. Stop by the right candle mounted on the wall, ensuring you are positioned without blocking any pathways. |
| **4.** Begin by leaving the room and turning to your right. Proceed down the hallway, be careful of any human activity or objects along the way. As you continue, look for the first doorway on your right. Enter through this doorway and advance towards the shelves. Once you reach the vicinity of the shelves, come to a halt and wait there. During this movement, avoid any obstacles or disruptions in the environment. |

*(Purple indicates human movements; Blue indicates agent-human interactions).*

#### HA-R2R Instruction Generation

To generate new instructions for the **HA-R2R dataset**, we employ **ChatGPT-4o** and **LLaMA-3-8B-Instruct** to **contextually enrich and expand scene information** based on the original instructions from the **R2R-CE dataset**.

**Few-Shot Prompting Approach**  
Our approach utilizes a **few-shot template prompt**, consisting of:
- **A system prompt** 
- **A set of few-shot examples** 

The **system prompt** primes the LLMs with the **context and requirements** for generating **navigation instructions** in human-populated environments. It outlines the **desired characteristics**, such as:
- **Relevance** to the navigation task,
- **Integration of human activities and agent interactions**, and
- **Precision in describing environmental details**.

The **few-shot examples** serve as **guidelines** for how the instructions should be structured, demonstrating:
- **Incorporation of human activities**,
- **Use of relative position information**, and
- **Integration with original navigation instructions**.

For instance, one **example** includes:
> *“You will notice someone quietly making a phone call, so please remain quiet as you move.”*

**Iterative Refinement Process**  
Initially, the models produced **irrelevant or subjective content** and lacked sufficient **detail about human activities**. To improve this:
1. We **reviewed outputs** and identified discrepancies.
2. We **refined the system prompt** to emphasize **neutral tone** and **avoid subjective descriptions**.
3. We **updated few-shot examples** to demonstrate **desired level of detail**.
4. Through multiple iterations, we ensured that **scene-enriched instructions** remained coherent and relevant to **HA-R2R**.

**LLM Prompt for HA-R2R Instruction Generation**

```json
{
  "system": "You are tasked with generating an objective and detailed description of a path and the related scene information based on the given input. Focus solely on observable entities and actions in the scene, avoiding descriptions of smell, atmosphere, or subjective feelings. Ensure clarity and precision in object and human activity descriptions.",
  "examples": "... //examples in Listing 4",
  "user": "Input:\n[instruction_text]: \"...\";\n[start]: \"...\";\n[during]: \"...\";\n[end]: \"...\";\n\nPlease provide an objective, step-by-step description of the path, focusing on the objects and human activities observed at each stage of the navigation (beginning, during, and end). Expand your description by including character actions, objective descriptions of objects, and details of the movement process. Your description should maintain a neutral tone and avoid embellishments. Please simulate the robot's movement along the path, while incorporating possible connections or interactions between the robot, objects, and human activities.\n\nOutput: ... //generation"
}

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

### 5. Human Activities Annotation Pipeline

#### Stage 1: Coarse Annotation
- **Goal:** Assign human motions to specific **regions** and **objects** using a **coarse-to-fine approach**.
- **Process:**
  - Filter human motions $\mathbf{H}$ based on region $\mathbf{R}$ and object list $\mathbf{O}$.
  - Match motions $h_i$ with objects $j_i$ using **semantic similarity**.
  - Optimize human placements $\mathbf{p}_{\text{opt}}^{h_i}$ using **Particle Swarm Optimization (PSO)**.  
- **Constraints:**
  - Search space limited by **region boundaries**.
  - Maintain **minimum safe distance** $\epsilon = 1\text{m}$ from other objects.
  - Ensures **naturalistic human placements** for training navigation agents.

#### Stage 2: Fine Annotation
- **Inspired by:** Real-world **3D skeleton tracking** techniques.
- **Setup:**
  - **9 RGB cameras** surround each human model to refine **position & orientation**.
  - **Multi-view capture** to correct **clipping issues** with surrounding objects.
- **Camera Angles:**
  - **8 side cameras:** $\theta_{\text{lr}}^{i} = \frac{\pi i}{8}$, alternate **up/down tilt**.
  - **1 overhead camera:** $\theta_{\text{ud}}^{9} = \frac{\pi}{2}$.
- **Scale:** 529 human models annotated in **374 regions** across **90 scans**.

#### Multi-Human Interaction & Motion Enrichment
- **Goal:** Increase **scene diversity** and **human interactions**.
- **Process:**
  - Use **LLMs** to generate new multi-human interactions.
  - **Manual refinement (4 rounds)** ensures consistency.
  - Place new motions relative to objects & use **multi-camera annotation**.
- **Result:**  
  - **910 human models** across **428 regions**.
  - **Complex motions**: Walking downstairs, climbing stairs.
  - **Interaction stats:** 72 **two-human pairs**, 59 **three-human pairs**, 15 **four-human groups**.
- **Impact:** Enables precise **social modeling** for human-aware navigation.

<div align="center">
  <img src="demo/figs/dataset_analy.png" alt="image" width="500"/>
</div>

---

## 🤖 HA-VLN-CMA Baseline Agent (agent)

The **HA-VLN-CMA** agent provides a baseline vision-and-language policy for continuous environments with dynamic multi-human interactions.

### 1. Policy Architecture

The policy (`CMAPolicy` in `agent/VLN-CE`) combines:
- **Instruction Encoder**: Bidirectional GRU encoder for language navigation commands.
- **Cross-Modal Attention (CMA)**: Jointly attends over visual RGB-D observations and instruction tokens.
- **Progress Monitor**: Predicts normalized distance to the navigation goal to aid action selection.

### 2. Agent Setup & Dependencies

To install the agent dependencies in your Python environment:

```bash
cd "$HA_VLN_ROOT"
python -m pip install -r requirements-py38.txt
```

Depth observations are encoded using a PointGoal pre-trained ResNet (`Data/ddppo-models/gibson-2plus-resnet50.pth`).

#### Pretrained Baseline Checkpoint

To evaluate our released pretrained HA-VLN-CMA model directly without training from scratch, obtain and place the released checkpoint:

```bash
# 1. Download checkpoint from Hugging Face (if not already downloaded in Quick Start)
huggingface-cli download fly1113/HA-VLN --include "checkpoints/*" --local-dir Data --repo-type dataset

# 2. Place checkpoint into the agent directory
mkdir -p agent/VLN-CE/data/checkpoints/cma_pm_da_aug_tune
cp Data/checkpoints/HA-VLN-CMA/ckpt.39.pth agent/VLN-CE/data/checkpoints/cma_pm_da_aug_tune/CMA_PM_DA_Aug.pth
```

### 3. Training from Scratch

To train the HA-VLN-CMA agent using DAgger imitation learning:

```bash
cd agent
python run.py --exp-config config/cma_pm_da_aug_tune.yaml --run-type train
```

### 4. Evaluation & Validation

To evaluate the policy on the validation split:

```bash
cd agent
python run.py --exp-config config/cma_pm_da_aug_tune.yaml --run-type eval
```

*(For expected baseline metrics on val_seen and val_unseen splits, see [Expected Benchmark Validation Results](#expected-benchmark-validation-results).)*

### 5. Test Inference & Submission

To run inference on the test split and export trajectories for submission:

```bash
cd agent
python run.py --exp-config config/cma_pm_da_aug_tune.yaml --run-type inference
```

---

## Contributing

We welcome contributions to this project! Please contact yfeidong@uw.edu , fyiwu@uw.edu , or bohanx2@uw.edu.

## Citation

If you find this repository or our paper useful, please consider **starring** this repository and **citing** our paper:

```bibtex
@misc{dong2025havln20openbenchmark,
      title={HA-VLN 2.0: An Open Benchmark and Leaderboard for Human-Aware Navigation in Discrete and Continuous Environments with Dynamic Multi-Human Interactions}, 
      author={Yifei Dong and Fengyi Wu and Qi He and Zhi-Qi Cheng and Heng Li and Minghan Li and Zebang Cheng and Yuxuan Zhou and Jingdong Sun and Qi Dai and Alexander G Hauptmann},
      year={2025},
      eprint={2503.14229},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2503.14229}, 
}
```

## License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.

---

