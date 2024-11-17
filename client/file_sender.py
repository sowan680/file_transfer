import asyncio
import os
import logging
from .chunk_manager import ChunkManager
from .state_manager import StateManager
from .network_module import NetworkModule
import aiohttp
import sys
from tenacity import RetryError

# Set up logging
logging.basicConfig(
    level=logging.INFO,  # Устанавливаем минимальный уровень логов для отображения
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат логов
    handlers=[logging.StreamHandler(sys.stdout)]  # Обработчик для вывода логов в консоль
)

class FileSender:
    def __init__(self, server_address, filepath):
        self.server_address = server_address
        self.filepath = filepath
        self.chunk_manager = None

    async def get_remote_file_size(self, filename):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.server_address}/file_size", params={"filename": filename}) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["size"]
                else:
                    logging.error(f"Failed to get file size for {filename}, server responded with {response.status}")
                    return 0

    async def start_transfer(self):
        if not self.filepath:
            logging.warning("No file specified for upload.")
            return

        filename = os.path.basename(self.filepath)
        logging.info(f"Selected file: {self.filepath}")
        self.chunk_manager = ChunkManager(self.filepath)
        chunk_size = self.chunk_manager.CHUNK_SIZE

        total_chunks = self.chunk_manager.total_chunks
        logging.info(f"Starting to send file in {total_chunks} chunks.")

        # Определяем, с какого индекса начать загрузку
        remote_file_size = await self.get_remote_file_size(filename)
        start_index = remote_file_size // chunk_size

        for index in range(start_index, total_chunks):
            chunk = self.chunk_manager.get_chunk(index)
            logging.info(f"Sending chunk {index + 1}/{total_chunks}.")

            success = await NetworkModule.send_chunk(
                self.server_address, chunk, index, filename, chunk_size
            )
            if success:
                logging.info(f"Chunk {index + 1} sent successfully.")
            else:
                logging.error(f"Failed to send chunk {index + 1}. Stopping transfer.")
                return

        # Завершаем загрузку
        try:
            await NetworkModule.complete_transfer(self.server_address, filename)
            logging.info("File transfer complete.")
        except Exception as e:
            logging.error(f"An error occurred during transfer completion: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python file_sender.py <path_to_file>")
        sys.exit(1)
    
    server_address = "http://server:8000"
    filepath = sys.argv[1]
    sender = FileSender(server_address, filepath)
    asyncio.run(sender.start_transfer())
