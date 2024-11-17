from fastapi import FastAPI, UploadFile, File, HTTPException
from connection_handler import ConnectionHandler
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()
handler = ConnectionHandler()

@app.post("/upload")
async def upload_chunk(index: int, filename: str, chunk_size: int, file: UploadFile = File(...)):
    logging.info(f"Received request to upload chunk {index} for file {filename} with chunk size {chunk_size}.")
    response = await handler.handle_upload(file, index, filename, chunk_size)
    return response

@app.post("/complete")
async def complete_transfer(filename: str):
    logging.info(f"Received request to finalize file transfer for {filename}.")
    return handler.finalize_transfer(filename)

@app.get("/file_size")
async def get_file_size(filename: str):
    size = handler.get_file_size(filename)
    logging.info(f"File size for {filename} is {size} bytes.")
    return {"size": size}