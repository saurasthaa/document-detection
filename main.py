import logging
import os
import time
from typing import List

import uvicorn
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uvicorn.config import LOGGING_CONFIG

from app.constants.constants import TEMP_OUTPUT_DIR, FASTAPI_OUTPUT_DIR
from app.engine.detect import detect
from app.utils.commons import create_directory

logging.basicConfig(level=logging.INFO)
load_dotenv()

app = FastAPI(title="Bitskraft Document Detection API", version="0.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

temp_video_dir: str = os.path.join(os.path.dirname(__file__), TEMP_OUTPUT_DIR)
create_directory(temp_video_dir)

image_save_path: str = os.path.join(
    os.path.dirname(__file__), FASTAPI_OUTPUT_DIR)
create_directory(image_save_path)


class DocumentAnalysisResponse(BaseModel):
    message: str
    meeting_id: str
    file_paths: List
    time_taken: float


def detect_document(video_path, meeting_id):
    try:
        start_time = time.time()
        results = detect(video_path, image_save_path)
        end_time = time.time()

        os.remove(video_path)

        if not results:
            response = DocumentAnalysisResponse(
                message="No Document Detected",
                meeting_id=meeting_id,
                file_paths=[],
                time_taken=round(end_time - start_time, 2),
            )
        else:
            response = DocumentAnalysisResponse(
                message="Success",
                meeting_id=meeting_id,
                file_paths=results,
                time_taken=round(end_time - start_time, 2),
            )

        logging.info(f"========== Response ==========\n{response}")

    except Exception as e:
        logging.error(e)
        response = DocumentAnalysisResponse(
            message=e,
            meeting_id=meeting_id,
            file_paths=[],
            time_taken=round(end_time - start_time, 2),
        )

    return response

    # response = requests.post(os.environ.get(
    #     "MIKHA_URI"), data=results, headers=headers)
    # logging.info(
    #     f"Response code: {response.status_code}\nResponse msg: {response.content}")


@app.post("/video-process")
async def process_video(id: str, video: UploadFile, background_tasks: BackgroundTasks):
    valid_video_extensions = (".mp4", ".avi", ".webm")
    if not video.filename.endswith(valid_video_extensions):
        logging.error(
            f"The file '{video.filename}' has an invalid extension. "
            f"Valid extensions are: {', '.join(valid_video_extensions)}"
        )

        return DocumentAnalysisResponse(
            message="Incorrect file format",
            meeting_id=id,
            file_paths=[],
            time_taken=0.0,
        )

    video_path = os.path.join(temp_video_dir, video.filename)

    video_content = video.file.read()

    with open(video_path, "wb") as f:
        f.write(video_content)

    background_tasks.add_task(detect_document, video_path, meeting_id=id)
    return {"message": "Your request is being processed", "id": id}


@app.get("/images/{fpath:path}", tags=["default"])
def image_download(fpath: str):
    if not os.path.exists(fpath):
        raise HTTPException(status_code=404, detail='File not found')
    return FileResponse(fpath)


if __name__ == "__main__":
    LOGGING_CONFIG["formatters"]["default"][
        "fmt"
    ] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    LOGGING_CONFIG["formatters"]["access"][
        "fmt"
    ] = '%(asctime)s [%(name)s] %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    uvicorn.run(app, host="0.0.0.0", port=6868)
