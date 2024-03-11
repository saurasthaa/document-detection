import glob
import os
import queue
import time
from typing import Tuple

import av
import cv2
import streamlit as st
import torch
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator

from app.constants.constants import (FONT, HEIGHT, MODEL_PATH,
                                     STREAMLIT_OUTPUT_DIR, TEXT_ORIGIN,
                                     TIMER_DURATION, WIDTH)
from app.utils.commons import generate_random_id, move_images

detect_model_path = os.path.join(os.path.dirname(__file__), MODEL_PATH)

image_save_path = os.path.join(os.path.dirname(__file__), STREAMLIT_OUTPUT_DIR)

if not os.path.exists(image_save_path):
    os.mkdir(image_save_path)

model = YOLO(detect_model_path)

i = 0
captured = False
capture_time = None


def remove_images():
    for col in cols:
        col.empty()


def bounding_box_points(shape: Tuple):
    cx = shape[1] // 2
    cy = shape[0] // 2
    x = int(cx - WIDTH / 2)
    y = int(cy - HEIGHT / 2)

    top_left = (x, y + 100)
    bottom_right = (x + WIDTH, y + HEIGHT + 180)

    return top_left, bottom_right


def save_image(img):
    num_images_captured = glob.glob(f"{image_save_path}/*.jpg")
    if len(num_images_captured) >= 10:
        return True
    else:
        file_id = generate_random_id() + ".jpg"
        file_name = image_save_path + "/" + file_id
        cv2.imwrite(str(file_name), img)
        return False


result_queue = queue.Queue()


def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    global i, captured, capture_time

    i += 1

    if i % 5 == 0:
        original_img = frame.to_ndarray(format="bgr24")
        img = original_img.copy()
        if captured:
            if capture_time is None:
                capture_time = time.time()

            if time.time() - capture_time <= TIMER_DURATION:
                cv2.putText(img, "Captured!", TEXT_ORIGIN, FONT, 0.8, (128, 255, 0), 1)
                return av.VideoFrame.from_ndarray(img, format="bgr24")
            else:
                i = 0
                captured = False
                capture_time = None
                move_images(image_save_path)

        result = model.predict(original_img)

        top_left, bottom_right = bounding_box_points(img.shape)
        actual_bbox = torch.Tensor(
            [top_left[0], top_left[1], bottom_right[0], bottom_right[1]]
        )
        predicted_bbox = torch.Tensor([0, 0, 0, 0])

        img = cv2.rectangle(
            img, pt1=top_left, pt2=bottom_right, color=(0, 0, 255), thickness=2
        )

        annotator = Annotator(img)
        boxes = result[0].boxes

        if boxes:
            for box in boxes:
                c = box.cls
                if c.item() == 0:
                    predicted_bbox = box.xyxy[0]
                    annotator.box_label(predicted_bbox, model.names[int(c)])
                    img = annotator.result()

                    # checking if the detected document is inside the frame
                    is_document_in_bbox = torch.isclose(
                        actual_bbox, predicted_bbox.cpu(), atol=0.05, rtol=0.05
                    )

                    if torch.all(is_document_in_bbox):
                        cv2.rectangle(
                            img,
                            pt1=top_left,
                            pt2=bottom_right,
                            color=(0, 255, 0),
                            thickness=2,
                        )
                        cv2.putText(
                            img,
                            "Document Detected!! Capturing...",
                            TEXT_ORIGIN,
                            FONT,
                            0.8,
                            (128, 255, 0),
                            1,
                        )

                        captured = save_image(original_img)

                        if not captured:
                            result_queue.put(original_img)

                        return av.VideoFrame.from_ndarray(img, format="bgr24")
                else:
                    cv2.putText(
                        img,
                        "Adjust document in the rectangle",
                        TEXT_ORIGIN,
                        FONT,
                        0.8,
                        (0, 0, 255),
                        1,
                    )
                    return av.VideoFrame.from_ndarray(img, format="bgr24")

        cv2.putText(
            img, "Document Not Detected!!", TEXT_ORIGIN, FONT, 0.8, (0, 0, 255), 1
        )

        return av.VideoFrame.from_ndarray(img, format="bgr24")


st.header("Document Detection")

webrtc_ctx = webrtc_streamer(
    key="object-detection",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
)

st.divider()

num_cols = 0
cols = st.columns(5)

if webrtc_ctx.state.playing:
    st.button("Clear", type="primary", on_click=remove_images)

while webrtc_ctx.state.playing:
    if not result_queue.empty():
        result = result_queue.get()
        cols[num_cols].image(result, use_column_width=True, channels="BGR")
        num_cols += 1

        if num_cols > 4:
            num_cols = 0

    time.sleep(0.08)
