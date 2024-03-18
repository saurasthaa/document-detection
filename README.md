# Document Detection

This repository contains code for a document detection application that detects documents within images or frames and captures the identified document areas. It provides a FastAPI server for real-time document detection and a Streamlit application for interactive document detection.

## Directory Structure

```
.
└── document-detection /
    ├── app/
    │   ├── __init__.py
    │   ├── constants
    │   ├── engine
    │   ├── model
    │   ├── routers
    │   └── utils
    ├── run.sh
    ├── .dockerignore
    ├── Dockerfile
    ├── requirements.txt
    ├── README.md
    ├── setup.py
    ├── main.py
    └── streamlit_demo.py
```

- **app/**: Contains the main codebase for the document detection application.
    - **constants/**: Directory for storing constants used across the application.
    - **engine/**: Directory containing the core detection engine.
    - **model/**: Directory for storing trained model.
    - **routers/**: Contains FastAPI routers for handling HTTP requests.
    - **utils/**: Directory for utility functions and helper code.
- **run.sh**: Script to run both FastAPI server and Streamlit application concurrently.
- **.dockerignore**: Specifies files and directories to be excluded when building Docker images.
- **Dockerfile**: Defines the environment setup for Docker containerization.
- **requirements.txt**: Lists Python dependencies required for the application.
- **README.md**: This file, providing an overview of the repository and its contents.
- **setup.py**: Configuration file for project setup and packaging.
- **main.py**: Code to run the FastAPI server for real-time document detection.
- **streamlit_demo.py**: Code to run the Streamlit application for interactive document detection.

## Usage

### Running the Application Locally

1. Install dependencies listed in `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

3. Run the Streamlit application:

    ```bash
    streamlit run streamlit_demo.py
    ```

### Docker

You can also run the application using Docker:

1. Build the Docker image:

    ```bash
    docker build -t document-detection .
    ```

2. Run the Docker container:

    ```bash
    docker run -d -p 8000:8000 -p 8080:8080 --name document_container document-detection
    ```


