#!/usr/bin/env python3
"""
/*
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *	Name: mistral_3_8B_image_cli.py
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *	Purpose: Test Image Decode via ministral-3:8b-instruct-2512-fp16 under Ollama API
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *	Dependent Reference
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *  (01)Ollama
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *  (02)ministral-3:8b-instruct-2512-fp16
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *	Known Issues
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *	Methodology
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *	References
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *	MSDN documents
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *	Internal documents
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *	Internet documents
 *-------------------------------------------------------------------------------------------------------------------------------------->
*/
"""

# Import Module
import argparse
import base64
import json
import requests
import time
from datetime import timedelta

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "ministral-3:8b-instruct-2512-fp16"

def time_fmt(sec):
    return str(timedelta(seconds=sec)).split('.')[0] + "." + f"{sec:.3f}".split('.')[-1]

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def main():
    parser = argparse.ArgumentParser(description="Mistral-3 8B Image Inference CLI")
    parser.add_argument("--image", required=True, help="Image file path")
    parser.add_argument("--prompt", default="Describe this image", help="Text prompt (optional)")
    args = parser.parse_args()

    # Convert image to base64
    encoded = encode_image(args.image)

    payload = {
        "model": MODEL_NAME,
        "prompt": args.prompt,
        "images": [encoded],
        "stream": True
    }

    print(f"[INFO] Start Inference: {time_fmt(0)}")
    t_start_request = time.time()

    response_text = ""
    t_first_token = None

    with requests.post(OLLAMA_URL, json=payload, stream=True) as resp:
        resp.raise_for_status()

        for line in resp.iter_lines():
            if not line:
                continue

            try:
                data = json.loads(line.decode())
            except:
                continue

            token = data.get("response", "")

            if token:
                if t_first_token is None:
                    t_first_token = time.time()
                    print(f"[INFO] Start Responding: {time_fmt(t_first_token - t_start_request)}")

                response_text += token

            if data.get("done", False):
                break

    t_end = time.time()
    print(f"[INFO] Finish Responding: {time_fmt(t_end - t_start_request)}")

    print("\n[Response]")
    print(response_text.strip())


if __name__ == "__main__":
    main()
