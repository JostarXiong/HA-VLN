# Environment Setup & Installation Guide

This guide provides comprehensive instructions for deploying the **HA-VLN 2.0** environment:
- **[1. Docker Environment (Recommended)](#docker-environment)**: Zero-configuration deployment with pre-built Habitat-Sim and CUDA runtime.
- **[2. Native Conda Installation (Python 3.8 / CUDA 11.8)](#native-conda-installation)**: Alternative local environment if you prefer not to use Docker.
- **[3. Dataset Acquisition](#dataset-acquisition)**: Setting up Matterport3D meshes and Hugging Face assets.
- **[4. Verification & Troubleshooting](#verification-troubleshooting)**: Headless rendering sanity checks and common fixes.

---

<a id="docker-environment"></a>
<a id="1-docker-environment-recommended"></a>
## 1. Docker Environment (Recommended)

Our official Docker image pre-configures CUDA 11.8, PyTorch 2.0.1, Habitat-Sim 0.1.7, Habitat-Lab 0.1.7, and headless graphics drivers (`libEGL`, `libGLX`), enabling out-of-the-box execution across Linux and WSL2 without host driver conflicts.

### Pull Docker Image

```bash
IMAGE=ghcr.io/jostarxiong/havln-challenge-2026@sha256:78a62cd176d2fd7d0e2825f4cb5be2488ebc5f1a354649b7b4f536a98f1054f4
docker pull "$IMAGE"
```

### Launch Interactive Container

```bash
DATA_DIR="$(cd Data && pwd -P)"

docker run --gpus all -it --rm \
  --shm-size 16g \
  --mount type=bind,source="$(pwd)",target=/workspace/HA-VLN \
  --mount type=bind,source="$DATA_DIR",target=/workspace/HA-VLN/Data \
  --mount type=bind,source="$DATA_DIR",target=/data/havln2 \
  --workdir /workspace/HA-VLN \
  "$IMAGE" bash
```

> [!IMPORTANT]
> **Initialize CMA Dependencies**: Once inside the running interactive container, you must run `setup_docker_cma.sh` to install CMA dependencies and link `habitat_baselines` before executing any training or evaluation commands from [agent/README.md](agent/README.md).

```bash
# Inside the running container:
bash scripts/setup_docker_cma.sh
```

### Key Docker Flags Explained

- `--gpus all`: Grants container access to host NVIDIA GPUs for hardware-accelerated headless EGL rendering.
- `--shm-size 16g`: Allocates shared memory for PyTorch multi-worker dataloading and inter-process communication.
- `--mount type=bind,...`: Dual-mounts host `Data/` to both `/workspace/HA-VLN/Data` and `/data/havln2`, satisfying both legacy and current configuration paths without manual editing.

<a id="optional-setup-groundingdino-inside-docker-container"></a>
<details>
<summary><b>Optional: Setup GroundingDINO inside Docker Container</b></summary>
<br>

*Note: GroundingDINO is only required if you explicitly enable online human detection and counting (`TASK_CONFIG.SIMULATOR.HUMAN_COUNTING: True`). Standard navigation policies (such as HA-VLN-CMA) do not require GroundingDINO.*

Inside the running Docker container, install Git and build dependencies, then compile GroundingDINO with the container's CUDA 11.8 toolchain:

```bash
source /opt/conda/etc/profile.d/conda.sh
conda activate havlnce
cd /workspace/HA-VLN

# 1. Install git and CUDA development toolkit inside container
apt-get update && apt-get install -y --no-install-recommends git
conda install -c nvidia/label/cuda-11.8.0 -c conda-forge \
  cuda-toolkit gcc_linux-64=11 gxx_linux-64=11 sysroot_linux-64=2.17 -y
export CUDA_HOME="$CONDA_PREFIX"
export CC="$CONDA_PREFIX/bin/x86_64-conda-linux-gnu-gcc"
export CXX="$CONDA_PREFIX/bin/x86_64-conda-linux-gnu-g++"
export PATH="$CUDA_HOME/bin:$PATH"

# 2. Install GroundingDINO perception dependencies (transformers, timm, etc.)
python -m pip install -r requirements-dino-py38.txt

# 3. Clone and build GroundingDINO
git clone https://github.com/IDEA-Research/GroundingDINO.git HASimulator/GroundingDINO
git -C HASimulator/GroundingDINO checkout df5b48a3efbaa64288d8d0ad09b748ac86f22671
MAX_JOBS=2 python -m pip install --no-deps --no-build-isolation -e HASimulator/GroundingDINO

# 4. Download pre-trained weights
mkdir -p HASimulator/GroundingDINO/weights
curl -fL --retry 3 \
  https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth \
  -o HASimulator/GroundingDINO/weights/groundingdino_swint_ogc.pth
python -m pip check
```

</details>

---

<a id="native-conda-installation"></a>
<a id="2-native-conda-installation-python-38--cuda-118"></a>
<a id="2-native-conda-installation-python-38-cuda-118"></a>
## 2. Native Conda Installation (Python 3.8 / CUDA 11.8)

> [!NOTE]
> **Alternative to Docker**: This native conda environment is provided only if you prefer not to use Docker. You do **not** need to deploy both environments. If you are already running via Docker, you can skip this section entirely.

<details>
<summary><b>Click to expand Native Conda Installation Guide</b></summary>
<br>

The primary local environment uses Python 3.8 and CUDA 11.8 with pre-built Habitat-Sim and Habitat-Lab pinned to **0.1.7**:

```bash
HA_VLN_ROOT="$(pwd)"

# 1. Create and activate conda environment
conda create -n havlnce python=3.8 pip=24.0 -c conda-forge -y
conda activate havlnce

# 2. Install pre-built headless Habitat-Sim and system libraries
conda install -c aihabitat -c conda-forge \
  "habitat-sim=0.1.7=*headless*" "numpy=1.23.5" \
  python-lmdb libxcrypt libopengl libglx -y

# 3. Install PyTorch with CUDA 11.8 support
python -m pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 \
  --index-url https://download.pytorch.org/whl/cu118

# 4. Clone and install Habitat-Lab 0.1.7 in development mode
git clone --branch v0.1.7 https://github.com/facebookresearch/habitat-lab.git
cd habitat-lab
python setup.py develop --all
cd "$HA_VLN_ROOT"

# 5. Install Python 3.8 compatibility requirements (preserves torch 2.0.1 / torchvision 0.15.2)
python -m pip install -r requirements-py38.txt \
  --extra-index-url https://download.pytorch.org/whl/cu118
```

<details>
<summary><b>Build Headless Habitat-Sim from Source (C++ / EGL Fallback)</b></summary>
<br>

If you require custom Habitat-Sim modifications or pre-built conda binaries fail on your distribution:

```bash
git clone --branch v0.1.7 https://github.com/facebookresearch/habitat-sim.git
cd habitat-sim

sudo apt-get update && sudo apt-get install -y --no-install-recommends \
  libjpeg-dev libglm-dev libgl1-mesa-glx libegl1-mesa-dev mesa-utils xorg-dev freeglut3-dev

pip install -r requirements.txt
python setup.py install --headless
```

</details>

<a id="setup-groundingdino-for-human-counting-optional"></a>
<a id="setup-groundingdino-native"></a>
<details>
<summary><b>Setup GroundingDINO for Human Counting (Optional)</b></summary>
<br>

*Note: GroundingDINO is an optional simulator perception module for online human detection, observation logging, and human counting ([HASimulator/detector.py](HASimulator/detector.py)). Standard navigation policies (such as HA-VLN-CMA) do not require GroundingDINO.*

```bash
cd "$HA_VLN_ROOT"
conda install -c nvidia/label/cuda-11.8.0 -c conda-forge \
  cuda-toolkit gcc_linux-64=11 gxx_linux-64=11 sysroot_linux-64=2.17 -y
export CUDA_HOME="$CONDA_PREFIX"
export CC="$CONDA_PREFIX/bin/x86_64-conda-linux-gnu-gcc"
export CXX="$CONDA_PREFIX/bin/x86_64-conda-linux-gnu-g++"
export PATH="$CUDA_HOME/bin:$PATH"

# Install GroundingDINO perception dependencies
python -m pip install -r requirements-dino-py38.txt

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

<details>
<summary><b>Legacy Python 3.7 Native Environment</b></summary>
<br>

These commands retain the original software stack for historical reference. Please install `habitat-sim` before installing `habitat-lab`:

```bash
conda create -n havln-agent python=3.7 -y
conda activate havln-agent

# Install Habitat-Sim 0.1.7 (Headless)
conda install -c aihabitat -c conda-forge habitat-sim=0.1.7=py3.7_linux_headless_da39a3ee5e6b4b0d3255bfef95601890afd80709 -y

# Clone and install Habitat-Lab 0.1.7
git clone --branch v0.1.7 https://github.com/facebookresearch/habitat-lab.git
cd habitat-lab
pip install -r requirements.txt
pip install -r habitat_baselines/rl/requirements.txt
python setup.py develop --all
cd ..

# Agent packages (Python 3.7)
pip install torch==1.9.1+cu111 torchvision==0.10.1+cu111 -f https://download.pytorch.org/whl/torch_stable.html
pip install -r requirements.txt
```

<details>
<summary><b>Setup GroundingDINO for Python 3.7 (Optional)</b></summary>
<br>

```bash
HA_VLN_ROOT="${HA_VLN_ROOT:-$(pwd)}"
cd "$HA_VLN_ROOT"
python -m pip install "supervision==0.11.1" "addict==2.4.0" "yapf==0.40.2" "timm==0.9.12" \
  "transformers==4.30.2" "tokenizers==0.13.3" "huggingface-hub==0.16.4" "safetensors==0.3.1" "pycocotools" "ninja"
git clone https://github.com/IDEA-Research/GroundingDINO.git HASimulator/GroundingDINO
git -C HASimulator/GroundingDINO checkout df5b48a3efbaa64288d8d0ad09b748ac86f22671
sed -i 's/supervision==[0-9.]*/supervision==0.11.1/' HASimulator/GroundingDINO/requirements.txt
export CUDA_HOME=/usr/local/cuda
python -m pip install --no-deps -e HASimulator/GroundingDINO

mkdir -p HASimulator/GroundingDINO/weights
curl -fL --retry 3 \
  https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth \
  -o HASimulator/GroundingDINO/weights/groundingdino_swint_ogc.pth
```

</details>

</details>

</details>

---

<a id="dataset-acquisition"></a>
<a id="3-dataset-acquisition"></a>
## 3. Dataset Acquisition

All scene meshes, human activities, and baseline checkpoints reside in `Data/`.

### Matterport3D Scene Meshes (`Data/scene_datasets`)

Request access on the [Matterport3D Project Page](https://niessner.github.io/Matterport/) to receive your personal download script:

```bash
python3 /path/to/download_mp.py -o Data/scene_datasets --task_data habitat
# After task-data download finishes, press Ctrl-C at the prompt for the main dataset.
unzip Data/scene_datasets/v1/tasks/mp3d_habitat.zip -d Data/scene_datasets
```

Scene meshes must reside at `Data/scene_datasets/mp3d/<scan>/<scan>.glb`.

### HA-VLN Simulation Assets & Annotations

Large simulation assets (HAPS 2.0 dynamic human motion meshes, HA-R2R navigation episodes, and CMA baseline weights) are officially hosted on [**Hugging Face (fly1113/HA-VLN)**](https://huggingface.co/datasets/fly1113/HA-VLN). Multi-human placement metadata (`human_motion.json`) and collision evaluation baselines are fetched from the pinned GitHub repository commit.

The included downloader script automatically orchestrates and verifies downloads from both sources with SHA-256 integrity checks:

```bash
python scripts/download_hf.py --destination Data --target all
```

Or download individual components using the official [Hugging Face Hub CLI](https://huggingface.co/docs/huggingface_hub/guides/cli):

```bash
pip install huggingface-hub
hf download fly1113/HA-VLN --repo-type dataset --local-dir Data
```

<details>
<summary><b>Legacy Google Drive Download (Backward Compatibility)</b></summary>
<br>

For users relying on earlier release workflows or unable to access Hugging Face, simulation assets can also be retrieved via the legacy Google Drive mirror using `scripts/download_data.sh` (requires `gdown`):

```bash
pip install gdown
bash scripts/download_data.sh
```

</details>

---

<a id="verification-troubleshooting"></a>
<a id="4-verification-troubleshooting"></a>
<a id="4-verification--troubleshooting"></a>
## 4. Verification & Troubleshooting

Run the following sanity checks to verify that headless GPU rendering and PyTorch CUDA extensions operate properly:

```bash
# 1. Verify PyTorch CUDA availability
python -c "import torch; assert torch.cuda.is_available(), 'CUDA not available'; print('PyTorch CUDA OK:', torch.cuda.get_device_name(0))"

# 2. Verify Headless Habitat-Sim rendering
python -c "import habitat_sim; print('Habitat-Sim version:', habitat_sim.__version__)"

# 3. Test scene rendering & dynamic humans
# Headless verification (renders and saves a verification frame to scripts/test/demo_frame.png):
python scripts/demo.py --scan 1LXtFkjw3qL --headless

# Interactive keyboard control (W/A/D/Q; requires an active GUI display session or forwarded DISPLAY):
python scripts/demo.py --scan 1LXtFkjw3qL
```

### Common Issues

1. **`libEGL.so.1: cannot open shared object file`**: Install Mesa headless runtime:
   ```bash
   sudo apt-get install -y libegl1-mesa libgl1-mesa-glx libgl1-mesa-dri
   ```
2. **`CUDA initialization error`**: Verify NVIDIA drivers and container runtime:
   ```bash
   nvidia-smi
   ```
3. **Library Path**: Make sure `$CONDA_PREFIX/lib` precedes system paths in `$LD_LIBRARY_PATH` so conda-forge's `libEGL.so` and `libGLX.so` are linked.
