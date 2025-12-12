# Introduction
This article primarily introduces how to install Docker, Ollama and run Edge AI Models through Ollama on the AIB-NIAO-S Ubuntu 22.04 environment provided by Avalue Technology Inc.

# Docker - JetPack 5.x (R35.x)
How to install Docker when target device with NVIDIA JetPack 5.x. - [Docker_JetPack_5.x.md](./Docker_JetPack_5.x.md)

# Docker - JetPack 6.x (R36.x)
How to install Docker when target device with NVIDIA JetPack 6.x. - [Docker_JetPack_6.x.md](./Docker_JetPack_6.x.md)

# Docker - Ollama
How to install Docker Ollama. - [Docker_Ollama.md](./Docker_Ollama.md)

# Docker - Ollama - Llama3.2 Vision
How to run Llama3.2 Vision under Ollama. - [Docker_Ollama_Llama3_2_Vision.md](./Docker_Ollama_Llama3_2_Vision.md)

# Docker - Ollama - Ministral-3:8B Instruct-2512-FP16
How to run Ministral-3:8B Instruct-2512-FP16 under Ollama. - [Docker_Ollama_Ministral_3_8B_Instruct_2512_FP16.md](./Docker_Ollama_Ministral_3_8B_Instruct_2512_FP16.md)

# How to install Broswer
Because of Chromium/Firefox may have issue in the Jetson Ubuntu 22.04.
Please refer as follows way to install brave-browser for AIB-NIAO-S.

```bash
sudo apt install curl
sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg \
https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg


echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg arch=arm64] \
https://brave-browser-apt-release.s3.brave.com/ stable main" \
| sudo tee /etc/apt/sources.list.d/brave-browser-release.list

sudo apt update
sudo apt install brave-browser

# Start brave-browser
brave-browser
```
