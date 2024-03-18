FROM python:3.11-slim as build

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y \
    cmake \
    build-essential \
    libglib2.0-0 \
    libgl1-mesa-glx 


WORKDIR /document-detection

COPY requirements.txt .

RUN pip install --upgrade pip && \ 
    pip install -r requirements.txt

COPY . /document-detection

RUN pip install .

RUN chmod +x run.sh

CMD ["./run.sh"]




