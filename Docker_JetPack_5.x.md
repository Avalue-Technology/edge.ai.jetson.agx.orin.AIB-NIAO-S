# Introduction
This article primarily introduces how to install Docker on the AIB-NIAO-S Ubuntu 22.04 environment provided by Avalue Technology Inc.
As follows steps are suitable for JetPack 5.x (R35.x).

# How to confirm the JetPack version?
```bash
# Output content similar to the following:
# R36 (release), REVISION: 2.0, GCID: 35463670, BOARD: t186ref ...
# R36.2.0 → JetPack 6.0
# R35.4.1 → JetPack 5.1.2
# R35.3.1 → JetPack 5.1.1
# R34.* → JetPack 5.0
# R32.* → JetPack 4.x
cat /etc/nv_tegra_release
```

# Prerequisite
We can consider installing a preferred text editor, which can then be used for configuration settings during the installation process.
```bash
sudo apt update
sudo apt install nano
```

# External Storage
Because of NVIDIA Jetson AGX Orin 64 GB is using shared memory architecture. So we will recommand you to extend NVMe SSD for Docker Images, Containers...etc.
Besides, Edge AI Models can also take up a lot of disk space. 
Please refer to the following steps to expand the NVMe SSD storage, then install Docker, and ensure all relevant files are stored within the expanded NVMe SSD.

## Format External Storage - ext4
```bash
lsblk -f
sudo umount /dev/nvme0n1p1
sudo mkfs.ext4 /dev/nvme0n1p1 -F
```

## Configure External Storage Mounted Directory
```bash
sudo mkdir -p /media/ssd
```

## Mount External Storage
```bash
sudo mount /dev/nvme0n1p1 /media/ssd
```

## Configure External Storage Permission
```bash
sudo chown -R $USER:$USER /media/ssd
sudo chmod -R 755 /media/ssd
```

## Configure Host Hugging Face Cache Environment Variables
```bash
sudo nano ~/.bashrc
```

```
# Add it to the end of the existing content, Please change /media/ssd/hfcache to your external storage device path
export HF_HOME=/media/ssd/hfcache
export HUGGINGFACE_HUB_CACHE=/media/ssd/hfcache
export TRANSFORMERS_CACHE=/media/ssd/hfcache
```

```bash
# Reload Environment Variables
source ~/.bashrc
mkdir -p /media/ssd/hfcache
```

## Set up automatic mounting of external storage device at boot
```bash
# Output is similar as follows
# /dev/nvme0n1p1: UUID="332f27b8-5526-40e8-94e0-08df3a9717f7" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="a62dfc53-01"
sudo blkid

# Modify /etc/fstab
# Append a new line to the end of the `/etc/fstab` file, similar to the content below, but please make the necessary modifications based on the UUID found for your target device
# UUID=332f27b8-5526-40e8-94e0-08df3a9717f7  /media/ssd  ext4  defaults,nofail  0  2
sudo nano /etc/fstab

# Verify /etc/fstab changes
sudo mount -a
```

# Install - Docker
## Uninstall - Docker
To ensure the installation and setup process aligns with the documentation, if Docker has been previously installed, consider removing the existing installation first.
This will allow us to proceed with the Docker installation and configuration step by step.
```bash
sudo apt-get remove docker docker.io containerd runc
```

## Configure Docker Official Package Repository
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

## Update apt Source
```bash
sudo apt-get update
```

## Install Docker Engine, Compose Plugin
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## Install NVIDIA Container Runtime - Docker with GPU
```bash
sudo apt install -y nvidia-container-runtime
sudo apt install -y libnvidia-container1 libnvidia-container-tools
```

## Configure Docker - NVIDIA Container Runtime
```bash
sudo nano /etc/docker/daemon.json
```

```
{
    "data-root": "/media/ssd/docker",
	"log-driver": "json-file",
    "log-opts": {
        "max-size": "50m",
        "max-file": "3"
    }
	"default-runtime": "nvidia",
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    }
}
```

## Enable - Docker Service
```bash
sudo systemctl enable docker
```

## Add User - Docker
```bash
# Adding users to a group requires logging out or restarting for the changes to take effect
sudo usermod -aG docker $USER
```

## Configure Docker Temporary Directory
```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo nano /etc/systemd/system/docker.service.d/tmpoverride.conf
```

```
[Service]
Environment=TMPDIR=/media/ssd/docker_tmp
```

```bash
sudo mkdir -p /media/ssd/docker_tmp
sudo chmod 1777 /media/ssd/docker_tmp

echo 'export TMPDIR=/media/ssd/docker_tmp' | sudo tee -a /etc/environment

sudo reboot
```

## Configure Container Temporary Directory
```bash
sudo mkdir -p /media/ssd/containerd
sudo rsync -aP /var/lib/containerd/ /media/ssd/containerd/

sudo rm -rf /var/lib/containerd
sudo ln -s /media/ssd/containerd /var/lib/containerd
```

## Create SWAP - Avoid Build/Convert Model Out of Memory 
```bash
sudo fallocate -l 48G /media/ssd/swapfile
sudo chmod 600 /media/ssd/swapfile
sudo mkswap /media/ssd/swapfile
sudo swapon /media/ssd/swapfile

# Append a new line to the end of the `/etc/fstab` file, as below content
# /media/ssd/swapfile  none  swap  sw  0  0
sudo nano /etc/fstab
```

## Reference
### Check - Docker Version
```bash
docker --version
```

### Check - NVIDIA Container Runtime Version
```bash
nvidia-container-runtime --version
```

### Check - NVIDIA Container Runtime Information
```bash
sudo nvidia-container-cli info
```

### Verify Docker Container with GPU Support
```bash
docker run --rm --gpus all --runtime=nvidia ubuntu:22.04 ls /dev/nvhost-gpu
```