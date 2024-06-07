import numpy as np
from ultralytics import YOLO


class SpillDetector:
    def __init__(
            self,
            path_to_model: str
    ):
        self.spill_detector = YOLO(path_to_model)

    def detect(
            self,
            image: np.ndarray
    ) -> list[list[int]]:
        results = list(
            self.spill_detector.track(
                image,
                persist=True,
                stream=True,
                show=False,
                tracker="bytetrack.yaml",
                conf=0.5,
                verbose=False,
            )
        )
        bboxes = []

        for result in results:
            bboxes = result.boxes.xyxy.cpu().numpy().astype(int).tolist()
            classes = result.boxes.cls.cpu().numpy().astype(int).tolist()
            

        return bboxes, classes
