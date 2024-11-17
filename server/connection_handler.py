from fastapi import HTTPException
from chunk_receiver import ChunkReceiver
import logging

class ConnectionHandler:
    def __init__(self):
        self.chunk_receiver = ChunkReceiver()

    async def handle_upload(self, file, index, filename, chunk_size):
        logging.info(f"Handling upload for chunk {index} of file {filename}.")
        content = await file.read()
        
        if not content:
            logging.error(f"Received empty chunk for index {index}.")
            raise HTTPException(status_code=400, detail="Received empty chunk")

        if not await self.chunk_receiver.receive_chunk(content, index, filename, chunk_size):
            logging.error(f"Error receiving chunk {index} for file {filename}.")
            raise HTTPException(status_code=400, detail="Error receiving chunk")

        logging.info(f"Chunk {index} for file {filename} received successfully.")
        return {"status": "Chunk received"}

    def finalize_transfer(self, filename):
        logging.info(f"File {filename} assembled successfully.")
        return {"status": f"File {filename} assembly complete"}

    def get_file_size(self, filename):
        return self.chunk_receiver.get_file_size(filename)
