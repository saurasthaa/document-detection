import os
from typing import List, Union

import cv2
from ultralytics import YOLO
import torch

from app.constants.constants import MODEL_PATH
from app.utils.commons import (generate_random_id,
                               get_image_crops, save_image)

detect_model_path: str = os.path.join(
    os.path.dirname(__file__), "..", MODEL_PATH)

model = YOLO(detect_model_path)


def detect(video_path: str, image_save_path: str) -> Union[List, int]:
    """
    Detects documents in a video file.

    Args:
        video_path (str): Path to the input video file.

    Returns:
        List or int: If documents are detected and saved successfully, returns list of file paths.
                     If no documents are detected, returns 0.

    Raises:
        FileNotFoundError: If the specified video file is not found.
        Exception: If an unexpected error occurs during processing.
    """
    i = 0
    cap = cv2.VideoCapture(video_path)

    documents = []

    while True:
        ret, frame = cap.read()

        if (i + 1) % 50 == 0:
            result = model.predict(frame)
            boxes = result[0].boxes

            if boxes:
                for box in boxes:
                    c = box.cls
                    if c.item() == 0:
                        predicted_bbox = box.xyxy[0].round().to(
                            torch.int).tolist()
                        doc = get_image_crops(frame, [predicted_bbox])[0]
                        documents.append(doc)

        i += 1

        if not ret:
            break

    cap.release()

    if documents:
        file_name = image_save_path + "/" + generate_random_id()
        file_paths = save_image(documents, file_name)
        return file_paths
    else:
        print("here")
        return 0
