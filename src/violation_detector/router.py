import io
from base64 import b64decode

import numpy as np
from PIL import Image
from fastapi import APIRouter, HTTPException
from loguru import logger

from settings import settings
from src.violation_detector import schemas as schemas
from src.violation_detector.model import SpillDetector

router = APIRouter(
    prefix='/PPE_violation',
    tags=['PPE_violation'],
)

storage_dir = settings.storage_folder

model_path = settings.storage_folder.joinpath(settings.yolo_checkpoint)
model = SpillDetector(
    path_to_model=model_path
)


@router.post(
    '/detect',
    response_model=list[schemas.SpillDetectorOutput]
)
async def detect_ppe_violation(
        request_body: schemas.SpillDetectorInput,
) -> list[schemas.SpillDetectorOutput]:
    try:
        frame_data = b64decode(request_body.frame_b64)
        frame_bytes = io.BytesIO(frame_data)
        frame_pil = Image.open(frame_bytes)
        frame = np.array(frame_pil)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="Invalid base64 format or empty image")

    bboxes, classes = model.detect(frame)

    return [schemas.SpillDetectorOutput(bbox=bbox, cls = cls) for bbox, cls in zip(bboxes, classes)]


async def main():
    import cv2
    from base64 import b64encode
    video_link = 'test_data/00088.mp4'
    cap = cv2.VideoCapture(video_link)
    while True:
        ret, frame = cap.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        success, buffer = cv2.imencode('.jpg', frame_rgb)
        frame_b64 = b64encode(buffer).decode('utf-8')
        request_body = schemas.SpillDetectorInput(frame_b64=frame_b64)
        results = await detect_ppe_violation(request_body)
        for result in results:
            logger.debug(result)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
