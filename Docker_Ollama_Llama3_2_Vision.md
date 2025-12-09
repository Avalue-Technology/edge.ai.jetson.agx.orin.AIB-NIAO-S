# Start Ollama
```bash
docker run -d --name ollama \
  --network=host \
  --privileged \
  -v /media/ssd/ollama:/root/.ollama \
  ollama/ollama:latest

docker exec -it ollama bash
```

# Pull Llama3.2 Vision via Ollama
```bash
ollama pull llama3.2-vision
```

# Run Llama3.2 Vision via Ollama
```bash
ollama run llama3.2-vision
```

# Tutorial - Inference 4K Resolution Image
![Llama3.2-Vision_Tutorial.png](https://raw.githubusercontent.com/Avalue-Technology/edge.ai.jetson.agx.orin.AIB-NIAO-S/refs/heads/main/Examples/Llama3.2-Vision_Tutorial.png "Llama3.2-Vision_Tutorial.png")
