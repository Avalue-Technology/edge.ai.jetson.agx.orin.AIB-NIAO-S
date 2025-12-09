# Start Ollama
```bash
docker run -d --name ollama \
  --network=host \
  --privileged \
  -v /media/ssd/ollama:/root/.ollama \
  ollama/ollama:latest

docker exec -it ollama bash
```

# Pull Ministral-3:8B Instruct-2512-FP16 via Ollama
```bash
ollama pull ministral-3:8b-instruct-2512-fp16
```

# Run Ministral-3:8B Instruct-2512-FP16 via Ollama
```bash
ollama run ministral-3:8b-instruct-2512-fp16
```

# Tutorial - Inference Image
![mistral_3_8B_image_cli.01.png](https://raw.githubusercontent.com/Avalue-Technology/edge.ai.jetson.agx.orin.AIB-NIAO-S/refs/heads/main/Examples/mistral_3_8B_image_cli.01.png "mistral_3_8B_image_cli.01.png")

# Tutorial - Inference Text
![mistral_3_8B_text_cli.01.png](https://raw.githubusercontent.com/Avalue-Technology/edge.ai.jetson.agx.orin.AIB-NIAO-S/refs/heads/main/Examples/mistral_3_8B_text_cli.01.png "mistral_3_8B_text_cli.01.png")
