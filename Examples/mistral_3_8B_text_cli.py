#!/usr/bin/env python3
"""
/*
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *	Name: mistral_3_8B_text_cli.py
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *	Purpose: Test Text Inference via ministral-3:8b-instruct-2512-fp16 under Ollama API
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
import requests
import time
from datetime import timedelta

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "ministral-3:8b-instruct-2512-fp16"

def time_fmt(sec):
    return str(timedelta(seconds=sec)).split('.')[0] + "." + f"{sec:.3f}".split('.')[-1]

def main():
    parser = argparse.ArgumentParser(description="Mistral-3 8B Text Inference CLI")
    parser.add_argument("--prompt", required=True, help="Input text prompt")
    args = parser.parse_args()

    payload = {
        "model": MODEL_NAME,
        "prompt": args.prompt,
        "stream": True
    }

    # Time tracking
    t_start_request = time.time()

    print(f"[INFO] Start Inference: {time_fmt(0)}")

    response_text = ""
    t_first_token = None

    # Send request
    with requests.post(OLLAMA_URL, json=payload, stream=True) as resp:
        resp.raise_for_status()

        for line in resp.iter_lines():
            if not line:
                continue

            # Each stream line is JSON
            try:
                import json
                data = json.loads(line.decode())
            except Exception:
                continue

            token = data.get("response", "")

            if token:
                # First token arrival time
                if t_first_token is None:
                    t_first_token = time.time()
                    print(f"[INFO] Start Responding: {time_fmt(t_first_token - t_start_request)}")

                response_text += token

            # End of stream
            if data.get("done", False):
                break

    t_end = time.time()
    print(f"[INFO] Finish Responding: {time_fmt(t_end - t_start_request)}")

    print("\n[Response]")
    print(response_text.strip())

if __name__ == "__main__":
    main()
