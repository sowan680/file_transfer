pip install -r requirements.txt

uvicorn server.server:app --host 0.0.0.0 --port 8000

python client/file_sender.py
