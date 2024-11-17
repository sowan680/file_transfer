import os
import logging

class ChunkManager:
    CHUNK_SIZE = 5 * 1024 * 1024  # Размер чанка

    def __init__(self, filepath):
        self.filepath = filepath
        self.total_chunks = (os.path.getsize(filepath) + self.CHUNK_SIZE - 1) // self.CHUNK_SIZE

    def get_chunk(self, index):
        try:
            with open(self.filepath, 'rb') as f:
                f.seek(index * self.CHUNK_SIZE)
                return f.read(self.CHUNK_SIZE)
        except Exception as e:
            logging.error(f"Error reading chunk {index} from file {self.filepath}: {e}")
            return None
