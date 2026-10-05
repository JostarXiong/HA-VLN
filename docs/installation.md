# Environment Setup & Installation Guide

This guide provides comprehensive instructions for deploying the **HA-VLN 2.0** environment. We offer two primary paths:
1. **[Docker Environment (Recommended)](#1-docker-environment-recommended)**: Zero-configuration deployment with pre-built Habitat-Sim and CUDA runtime.
2. **[Native Conda Installation](#2-native-conda-installation-python-38--cuda-118---recommended)**: Flexible local environment for advanced development.

---

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

### Key Docker Flags Explained

- `--gpus all`: Grants container access to host NVIDIA GPUs for hardware-accelerated headless EGL rendering.
- `--shm-size 16g`: Allocates shared memory for PyTorch multi-worker dataloading and inter-process communication.
- `--mount type=bind,...`: Dual-mounts host `Data/` to both `/workspace/HA-VLN/Data` and `/data/havln2`, satisfying both legacy and current configuration paths without manual editing.

---

## 2. Native Conda Installation (Python 3.8 / CUDA 11.8 - Recommended)

The following Linux setup uses Python 3.8 and CUDA 11.8 PyTorch stack. Habitat-Sim and Habitat-Lab are pinned to **0.1.7**:

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

# 4. Clone and install Habitat-Lab v0.1.7
git clone --branch v0.1.7 --depth 1 \
  https://github.com/facebookresearch/habitat-lab.git habitat-lab
python -m pip install -c requirements-py38.txt \
  -r habitat-lab/requirements.txt setuptools pytest-runner \
  tensorboard moviepy webdataset ifcfg msgpack_numpy
python -m pip install --no-deps --no-build-isolation -e habitat-lab

# 5. Install Agent & Simulator dependencies
python -m pip install -r requirements-py38.txt

# 6. Configure environment variables for headless rendering
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:${LD_LIBRARY_PATH:-}"
export DISPLAY=""
export EGL_DEVICE_ID=0
```

---

## 3. Alternative: Build Habitat-Sim 0.1.7 from Source

Use this **instead of** the pre-built conda package if you need to modify simulator C++ source code or headers:

```bash
# 1. Install build dependencies and headless OpenGL headers
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
  cmake build-essential libjpeg-dev libglm-dev libgl1 \
  libegl1-mesa-dev mesa-utils xorg-dev freeglut3-dev

# 2. Clone Habitat-Sim v0.1.7 recursively
git clone --branch v0.1.7 --recursive \
  https://github.com/facebookresearch/habitat-sim.git habitat-sim
cd habitat-sim

# 3. Build and install with headless EGL support
python -m pip install -r requirements.txt -c "$HA_VLN_ROOT/requirements-py38.txt"
python setup.py install --headless
cd "$HA_VLN_ROOT"
```

---

## 4. Legacy Native Conda Setup (Python 3.7 / CUDA 11.1)

These commands retain the original software stack for historical reference. Please install `habitat-lab` (v0.1.7) and `habitat-sim` (v0.1.7) following [ETPNav](https://github.com/MarSaKi/ETPNav/):

```bash
conda create -n havlnce python=3.7 -y
conda activate havlnce
conda install -c aihabitat -c conda-forge habitat-sim=0.1.7 headless -y

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

---

## 5. GroundingDINO Setup for Human Counting (Optional)

> **Note**: GroundingDINO is an optional simulator perception module for online open-set human detection, observation logging, and reward shaping ([HASimulator/detector.py](../HASimulator/detector.py)). Standard navigation policies (such as HA-VLN-CMA) do **not** require GroundingDINO.
> By default, human counting is disabled (`HUMAN_COUNTING: False`), and the official Docker image does not pre-install GroundingDINO.

### Setup for Python 3.8 / CUDA 11.8 (Recommended)

```bash
cd "$HA_VLN_ROOT"

# 1. Install pinned Python dependencies
python -m pip install -r requirements-dino-py38.txt

# 2. Install compatible host compiler and CUDA toolkit via conda
conda install -c nvidia/label/cuda-11.8.0 -c conda-forge \
  cuda-toolkit gcc_linux-64=11 gxx_linux-64=11 sysroot_linux-64=2.17 -y
export CUDA_HOME="$CONDA_PREFIX"
export CC="$CONDA_PREFIX/bin/x86_64-conda-linux-gnu-gcc"
export CXX="$CONDA_PREFIX/bin/x86_64-conda-linux-gnu-g++"

# 3. Clone GroundingDINO at pinned revision and compile
git clone https://github.com/IDEA-Research/GroundingDINO.git HASimulator/GroundingDINO
git -C HASimulator/GroundingDINO checkout df5b48a3efbaa64288d8d0ad09b748ac86f22671
MAX_JOBS=2 python -m pip install --no-deps --no-build-isolation \
  -e HASimulator/GroundingDINO

# 4. Download pre-trained Swin-T detector weights
mkdir -p HASimulator/GroundingDINO/weights
curl -fL --retry 3 \
  https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth \
  -o HASimulator/GroundingDINO/weights/groundingdino_swint_ogc.pth

python -m pip check
```

### Setup for Legacy Python 3.7 / CUDA 11.1

```bash
# Requires system CUDA 11.1 toolkit and compatible gcc
python -m pip install -r requirements-dino-py38.txt
export CUDA_HOME=/usr/local/cuda

git clone https://github.com/IDEA-Research/GroundingDINO.git HASimulator/GroundingDINO
git -C HASimulator/GroundingDINO checkout df5b48a3efbaa64288d8d0ad09b748ac86f22671
pip install --no-deps --no-build-isolation -e HASimulator/GroundingDINO

mkdir -p HASimulator/GroundingDINO/weights
curl -fL --retry 3 \
  https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth \
  -o HASimulator/GroundingDINO/weights/groundingdino_swint_ogc.pth
```

### Enabling in Task Configuration

To activate human counting during evaluation, update [HASimulator/config/HAVLNCE_task.yaml](../HASimulator/config/HAVLNCE_task.yaml):

```yaml
SIMULATOR:
  HUMAN_COUNTING: True
```

---

## 6. Headless Rendering & Display Troubleshooting

When running without an X server (headless GPU servers or WSL2):
1. **EGL Configuration**: Ensure `export EGL_DEVICE_ID=0` is set to match your primary GPU.
2. **Empty DISPLAY**: Keep `export DISPLAY=""` so Habitat-Sim automatically binds to EGL rather than attempting GLX through an absent X11 server.
3. **Library Path**: Make sure `$CONDA_PREFIX/lib` precedes system paths in `$LD_LIBRARY_PATH` so conda-forge's `libEGL.so` and `libGLX.so` are linked.
