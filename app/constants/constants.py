from pathlib import Path

import cv2

MODEL_PATH = "model/best.pt"

# Detection Constants
WIDTH = 200
HEIGHT = 80
TEXT_ORIGIN = (20, 20)
FONT = cv2.FONT_HERSHEY_SIMPLEX
TIMER_DURATION = 5

STREAMLIT_OUTPUT_DIR = "streamlit_preds"
FASTAPI_OUTPUT_DIR = "fastapi_preds"
