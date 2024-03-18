from typing import Tuple

import cv2

MODEL_PATH: str = "model/best.pt"

# Detection Constants
WIDTH: int = 200
HEIGHT: int = 80
TEXT_ORIGIN: Tuple[int, int] = (20, 20)
FONT = cv2.FONT_HERSHEY_SIMPLEX
TIMER_DURATION: int = 5

STREAMLIT_OUTPUT_DIR: str = "assets/streamlit_preds"
FASTAPI_OUTPUT_DIR: str = "assets/fastapi_preds"
TEMP_OUTPUT_DIR: str = "assets/temp"
