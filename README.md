# Introduction
This article primarily introduces how to install Docker, Ollama, Llama3.2 Vision on the AIB-NIAO-S Ubuntu 22.04 environment provided by Avalue Technology Inc.

# Prerequisite
We can consider installing a preferred text editor, which can then be used for configuration settings during the installation process.
```bash
sudo apt update
sudo apt install nano
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

# Install - Ollama
## Instal - Ollama Docker
```bash
docker pull ollama/ollama:latest
```

## Start Ollama with GPU
```bash
docker run -d --gpus all -p 11434:11434 -v ollama:/root/.ollama --name ollama ollama/ollama:latest
```

## Pull Llama3.2 Vision via Ollama
```bash
docker exec -it ollama ollama pull llama3.2-vision
```

## Configure SWAP (avoid Out of Memory)
```bash
# Extend SWAP
sudo fallocate -l 16G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

```bash
sudo nano /etc/fstab
```

```
# Add a new column as follows
/swapfile   none    swap    sw    0   0
```

## Configure - Maximum Performance
```bash
sudo nano /etc/systemd/system/jetson-performance.service
```

```
[Unit]
Description=Max performance for Jetson
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/usr/sbin/nvpmodel -m 0
ExecStart=/usr/bin/jetson_clocks
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable jetson-performance
sudo systemctl start jetson-performance
```

## Create Ollama Docker Compose YAML
```bash
mkdir -p /home/nvidia/ollama
sudo nano /home/nvidia/ollama/ollama-docker-compose.yaml
```

```
version: "3.9"

services:
  ollama:
    container_name: ollama
    image: ollama/ollama:latest
    restart: always
    volumes:
      - ollama:/root/.ollama
    ports:
      - "11434:11434"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              capabilities: [gpu]
    environment:
      - OLLAMA_HOST=0.0.0.0

volumes:
  ollama:
```

## Create Ollama Docker Service (For run automatically at startup)
```bash
sudo nano /etc/systemd/system/ollama-docker.service
```

```
[Unit]
Description=Ollama Docker Compose Service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
WorkingDirectory=/home/nvidia/ollama
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/usr/bin/docker compose -f /home/nvidia/ollama/ollama-docker-compose.yaml up -d
ExecStop=/usr/bin/docker compose -f /home/nvidia/ollama/ollama-docker-compose.yaml down
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable ollama-docker
sudo systemctl start ollama-docker
```

## Create Ollama Model Preload Shell Script
Preloading models can reduce the time required for the first inference.
```bash
sudo nano /home/nvidia/ollama/ollama-preload.sh
```

```
#!/bin/bash

echo "Waiting for Ollama API to become ready..."

# Wait up to 30 seconds
for i in {1..30}; do
    if curl -sf http://127.0.0.1:11434/api/version >/dev/null 2>&1; then
        echo "Ollama API is ready!"
        break
    fi
    echo "Not ready yet, retrying ($i)..."
    sleep 1
done

echo "Preloading model llama3.2-vision..."
docker exec ollama ollama run llama3.2-vision "Preloading model..."
```

```bash
sudo chmod +x /home/nvidia/ollama/ollama-preload.sh
```

## Create Ollama Model Preload Service
```bash
sudo nano /etc/systemd/system/ollama-preload.service
```

```

[Unit]
Description=Preload Llama3.2-Vision model into Ollama
After=ollama-docker.service
Requires=ollama-docker.service

[Service]
Type=oneshot
ExecStart=/home/nvidia/ollama/ollama-preload.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable ollama-preload
sudo reboot
```

# Reference
## Check - Ollama Model Preload Service
```bash
journalctl -u ollama-preload -n 50 --no-pager
```

## Configure - Auto Login
```bash
sudo nano /etc/gdm3/custom.conf
```
Please locate the following annotation content.
```
# AutomaticLoginEnable = true
# AutomaticLogin = user1
```
Please modify it to the following content.
```
AutomaticLoginEnable = true
AutomaticLogin = nvidia
```

```bash
sudo reboot
```

## Tutorial - Inference 4K Resolution Image
![Llama3.2-Vision_Tutorial.png](https://raw.githubusercontent.com/Avalue-Technology/edge.ai.jetson.agx.orin.AIB-NIAO-S/refs/heads/main/Examples/Llama3.2-Vision_Tutorial.png "Llama3.2-Vision_Tutorial.png")
