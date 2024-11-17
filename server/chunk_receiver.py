import os
import logging

class ChunkReceiver:
    def __init__(self, upload_dir="uploaded_videos"):
        self.upload_dir = upload_dir
        self.chunk_sizes = {}  # Словарь для хранения размера чанков для каждого файла
        os.makedirs(upload_dir, exist_ok=True)

    async def receive_chunk(self, content, index, filename, chunk_size):
        # Определяем путь сохранения файла
        filepath = os.path.join(self.upload_dir, filename)
        
        # Сохраняем размер чанка для файла, если он еще не был сохранен
        if filename not in self.chunk_sizes:
            self.chunk_sizes[filename] = chunk_size

        # Проверка соответствия переданного размера чанка с сохраненным значением
        if self.chunk_sizes[filename] != chunk_size:
            logging.error(f"Chunk size mismatch for file {filename}. Expected {self.chunk_sizes[filename]}, got {chunk_size}.")
            raise ValueError("Chunk size mismatch.")

        # Записываем чанк на нужную позицию в итоговом файле
        with open(filepath, 'r+b' if os.path.exists(filepath) else 'wb') as f:
            f.seek(index * chunk_size)
            f.write(content)
        
        logging.info(f"Stored chunk {index} for file {filename} at position {index * chunk_size}.")
        return True

    def get_file_size(self, filename):
        # Возвращаем размер уже собранного файла
        filepath = os.path.join(self.upload_dir, filename)
        return os.path.getsize(filepath) if os.path.exists(filepath) else 0