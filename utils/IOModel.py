from pydantic import BaseModel, Field
from typing import Any

class ImageChallengeModel(BaseModel):
    image: str = Field(..., pattern=r"^data:image\/[a-zA-Z]*;base64,.*$")
    challengeText: str

class PoseStates(BaseModel):
    left_eye_state: str
    right_eye_state: str
    mouth_state: str
    head_state: str

class ImageChallengeStatusModel(BaseModel):
    status: str
    pose_states: PoseStates
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "string",
                "pose_states": {
                    "left_eye_state": "string",
                    "right_eye_state": "string",
                    "mouth_state": "string",
                    "head_state": "string",
                },
            }
        }

class OutputModelMain(BaseModel):
    status: str
    api: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "string",
                "api": "string",
            }
        }

class OutputModelError(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "string"
            }
        }