#!/bin/sh

echo "Starting FastAPI server"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

echo "Starting Streamlit server"
streamlit run streamlit_demo.py --server.port 8080