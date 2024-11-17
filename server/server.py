from fastapi import FastAPI, UploadFile, File, HTTPException
from chunk_receiver import ChunkReceiver
import logging

# Конфигурация логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()
chunk_receiver = ChunkReceiver(upload_dir="uploaded_videos")

@app.post("/upload")
async def upload_chunk(index: int, filename: str, chunk_size: int, file: UploadFile = File(...)):
    logging.info(f"Received request to upload chunk {index} for file {filename} with chunk size {chunk_size}.")
    content = await file.read()
    
    if not content:
        logging.error(f"Received empty chunk for index {index}.")
        raise HTTPException(status_code=400, detail="Received empty chunk")

    try:
        await chunk_receiver.receive_chunk(content, index, filename, chunk_size)
        logging.info(f"Chunk {index} for file {filename} received successfully.")
        return {"status": "Chunk received"}
    except ValueError as e:
        logging.error(f"Error receiving chunk {index} for file {filename}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/complete")
async def complete_transfer(filename: str):
    unique_filename = chunk_receiver.get_unique_filename(filename)
    logging.info(f"File {unique_filename} assembled successfully.")
    return {"status": f"File {unique_filename} assembly complete"}

@app.get("/file_size")
async def get_file_size(filename: str):
    size = chunk_receiver.get_file_size(filename)
    logging.info(f"File size for {filename} is {size} bytes.")
    return {"size": size}
