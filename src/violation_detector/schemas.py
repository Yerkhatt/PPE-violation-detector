from pydantic import BaseModel


class SpillDetectorInput(BaseModel):
    frame_b64: str


class SpillDetectorOutput(BaseModel):
    bbox: list[int]
    cls: int