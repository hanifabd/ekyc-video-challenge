import cv2
import base64
import numpy as np
from PIL import Image
from io import BytesIO

def bgr2rgb(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def rgb2bgr(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image

def mirrorImage(image):
    image = cv2.flip(image, 1)
    return image

def base64_to_image(base64_str: str) -> np.ndarray:
    try:
        # Remove the data URI scheme if present
        if "," in base64_str:
            base64_str = base64_str.split(",")[1]

        # Decode the Base64 string
        decoded_data = base64.b64decode(base64_str)
        pil_image = Image.open(BytesIO(decoded_data))
        return np.array(pil_image)
    except Exception as e:
        raise Exception(f"Invalid Base64 image: {e}")

def checkChallengeStatus(challenge: str, states: dict) -> str:
    print(challenge)
    print(states)
    if challenge == "Left Eye Closed":
        if "Closed" in states.get("right_eye_state"):
            challenge_status = "Success"
        else:
            challenge_status = "Failed"
    elif challenge == "Right Eye Closed":
        if "Closed" in states.get("left_eye_state"):
            challenge_status = "Success"
        else:
            challenge_status = "Failed"
    elif challenge == "Face Forward":
        if "Forward" in states.get("head_state"):
            challenge_status = "Success"
        else:
            challenge_status = "Failed"
    elif challenge == "Face Left":
        if "Left" in states.get("head_state"):
            challenge_status = "Success"
        else:
            challenge_status = "Failed"
    elif challenge == "Face Right":
        if "Right" in states.get("head_state"):
            challenge_status = "Success"
        else:
            challenge_status = "Failed"
    elif challenge == "Face Down":
        if "Down" in states.get("head_state"):
            challenge_status = "Success"
        else:
            challenge_status = "Failed"
    elif challenge == "Face Up":
        if "Up" in states.get("head_state"):
            challenge_status = "Success"
        else:
            challenge_status = "Failed"
    elif challenge == "Mouth Open":
        if "Open" in states.get("mouth_state"):
            challenge_status = "Success"
        else:
            challenge_status = "Failed"
    else:
        challenge_status = "Invalid"
    
    return challenge_status