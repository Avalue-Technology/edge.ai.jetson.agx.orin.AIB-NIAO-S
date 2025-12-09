# Instal - Ollama Docker
```bash
docker pull ollama/ollama:latest
```

# Start Ollama with GPU
```bash
docker run -d --gpus all -p 11434:11434 -v ollama:/root/.ollama --name ollama ollama/ollama:latest
```

# Configure - Maximum Performance
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

# Create Ollama Docker Compose YAML
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

# Create Ollama Docker Service (For run automatically at startup)
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

# Create Ollama Model Preload Shell Script
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

# Create Ollama Model Preload Service
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
