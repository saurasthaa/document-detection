from ultralytics import YOLO
import torch
import os

from app.constants.constants import *
from utils import generate_random_id, move_images

detect_model_path = os.path.join(os.path.dirname(__file__), MODEL_PATH)

image_save_path = os.path.join(os.path.dirname(__file__), OUTPUT_DIR)

if not os.path.exists(image_save_path):
    os.mkdir(image_save_path)

model = YOLO(detect_model_path)


def detect():
    pass
