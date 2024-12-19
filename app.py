from project_docs import project_info
import os
import uuid
import datetime
import uvicorn
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utils.IOModel import ImageChallengeModel, ImageChallengeStatusModel, OutputModelMain, OutputModelError, PoseStates

import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

from utils.pose_detection.g_helper import base64_to_image, bgr2rgb, mirrorImage, checkChallengeStatus
from utils.pose_detection.fp_helper import pipelineHeadTiltPose, draw_face_landmarks_fp
from utils.pose_detection.ms_helper import pipelineMouthState
from utils.pose_detection.es_helper import pipelineEyesState

# Logging Settings
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Working Dir Settings
current_dir = os.getcwd()

# FastApi App Settings
app = FastAPI(**project_info.project_info())
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app_response_message = {
    500: {"model": OutputModelError}, # Internal Service Error Response Template
    405: {"model": OutputModelError}, # Method not Allowed Response Template
}

# Apps Start Log Information
log.info(f'''\n
[APP START] ********************************************************************
Loading model and starting server. Please wait until server has fully started
Started       : {datetime.datetime.now()}
Work Dir      : {current_dir}
********************************************************************************\n''')

# App Routes
# Main Route -----------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.get(
    "/", 
    response_model=OutputModelMain, # Swagger for Main Output Template
    responses=app_response_message # Swagger for Error Template
)
async def main():
    response = OutputModelMain(
        status="ok",
        api="face-pose-detection", # Api Identifier for Ngobrol-LLM
    )
    return response

# Challenge Route -----------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.post(
    "/facepose-challenge", # Route for Standard Response Scheme
    response_model=ImageChallengeStatusModel, # Swagger for LLMs Output Template
    responses=app_response_message # Swagger for Error Template
)
async def facepose_challenge(challenge_request: ImageChallengeModel):
    # Create request_id for Trace Log E2E Process in Route
    request_id = str(uuid.uuid4()) 
    request_body = challenge_request.dict()

    # Base64 to Image
    image_np = base64_to_image(request_body.get("image"))
    # Mirror image (Optional)
    image_np = mirrorImage(image_np)

     # Initialize FaceMesh
    with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
        # Process the image
        results = face_mesh.process(bgr2rgb(image_np))
        
        # Process face landmarks
        head_tilt_pose = "Undetected"
        mouth_state = "Undetected"
        r_eyes_state = "Undetected"
        l_eyes_state = "Undetected"
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # FACE MESH
                draw_face_landmarks_fp(image_np, face_landmarks)
                # HEAD TILT POSE
                head_tilt_pose = pipelineHeadTiltPose(image_np, face_landmarks)
                # MOUTH STATE
                mouth_state = pipelineMouthState(image_np, face_landmarks)
                # EYES STATE
                r_eyes_state, l_eyes_state = pipelineEyesState(image_np, face_landmarks)

    # Check Status Challenge Success or Not
    challenge_data = {
        "challenge": request_body.get("challengeText"),
        "states": {
            "left_eye_state": l_eyes_state,
            "right_eye_state": r_eyes_state,
            "mouth_state": mouth_state,
            "head_state": head_tilt_pose
        }
    }
    challenge_status = checkChallengeStatus(**challenge_data)

    try:
        response = ImageChallengeStatusModel(
            status=challenge_status,
            pose_states=PoseStates(
                left_eye_state=l_eyes_state,
                right_eye_state=r_eyes_state,
                mouth_state=mouth_state,
                head_state=head_tilt_pose
            )
        )
        return response
    except Exception as e:
        # Error Handling Block: General Error Information
        log.error(f"{datetime.datetime.now()} \033[93m[E] Error Exception {request_id}:\033[0m {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

# App Initialization ---------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":    
    log.info(f"{Path(__file__).stem}:app")
    uvicorn.run(f"{Path(__file__).stem}:app", port=8000, host="0.0.0.0")