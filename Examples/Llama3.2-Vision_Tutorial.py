"""
/*
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *	Name: Llama3.2-Vision_Tutorial.py
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *	Purpose: Test Llama3.2-Vision via Ollama API
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *	Dependent Reference
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *  (01)Ollama
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *  (02)Llama3.2-Vision
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *  (03)sudo apt install python3-pip
 *-------------------------------------------------------------------------------------------------------------------------------------->
 *  (04)sudo apt install python3-pil
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
import base64
import requests
import time
from PIL import Image
from io import BytesIO


def funResizeImageMax1024(strFileName):
    """Resize image so longest side <= 1024 px, keep aspect ratio"""

    # Load image
    objImage = Image.open(strFileName)

    # Get size
    intWidth, intHeight = objImage.size
    intMaxSide = max(intWidth, intHeight)

    # If already <=1024, no resize needed
    if intMaxSide <= 1024:
        bytImageBytes = BytesIO()
        objImage.save(bytImageBytes, format="JPEG")
        return bytImageBytes.getvalue()

    # Compute scale
    fltScale = 1024.0 / float(intMaxSide)
    new_width = int(intWidth * fltScale)
    new_height = int(intHeight * fltScale)

    # Resize using high-quality LANCZOS
    objImageResized = objImage.resize((new_width, new_height), Image.LANCZOS)

    # Convert to bytes
    bytImageBytes = BytesIO()
    objImageResized.save(bytImageBytes, format="JPEG")
    return bytImageBytes.getvalue()


def funConvertImageToBase64Bytes(binImageBytes):
    """Convert image bytes to Base64 string"""
    return base64.b64encode(binImageBytes).decode("utf-8")


def proInferenceImage(strFilename, strDescription):
    """Test Single Image Inference Speed via /api/chat"""

    print(f"\n==============================")
    print(f"Testing: {strDescription} ({strFilename})")
    print("==============================")

    # Resize Image
    bytResizedImage = funResizeImageMax1024(strFilename)

    # Convert to Base64
    strImageBase64String = funConvertImageToBase64Bytes(bytResizedImage)

    # API payload for /api/chat
    jsonPayload = {
        "model": "llama3.2-vision",
        "messages": [
            {
                "role": "user",
                "content": "Explain this image.",
                "images": [strImageBase64String]
            }
        ],
        "stream": False
    }

    # Start Time
    fltStartTime = time.time()

    # Call Ollama API
    objResponse = requests.post(
        "http://127.0.0.1:11434/api/chat",
        json=jsonPayload
    )

    # End Time
    fltEndTime = time.time()
    fltElapsed = fltEndTime - fltStartTime

    # Display Result
    print("\n--- Model Output ---")
    try:
        print(objResponse.json()["message"]["content"])
    except Exception as e:
        print("Error parsing response:", e)
        print("Raw response:", objResponse.text)

    print("\n--- Performance ---")
    print(f"{strDescription} Inference Time: {fltElapsed:.2f} seconds")


# Test 4K Resolution Image Inference
proInferenceImage("4K.jpg", "4K Resolution")
