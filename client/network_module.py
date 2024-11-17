import aiohttp
import logging
from tenacity import retry, stop_after_delay, wait_exponential, RetryError

class NetworkModule:
    @staticmethod
    @retry(stop=stop_after_delay(3600), wait=wait_exponential(multiplier=1, min=1, max=3600))
    async def send_chunk(server_address, chunk, index, filename, chunk_size):
        try:
            data = aiohttp.FormData()
            data.add_field('file', chunk, filename=f'chunk_{index}', content_type='application/octet-stream')

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{server_address}/upload", data=data, params={"index": index, "filename": filename, "chunk_size": chunk_size}
                ) as response:
                    if response.status == 200:
                        return True
                    else:
                        logging.error(f"Server responded with status code {response.status} for chunk {index}.")
                        raise Exception(f"Failed to send chunk {index+1}, server responded with {response.status}")
        except aiohttp.ClientError as e:
            logging.error(f"Connection error while sending chunk {index}: {e}")
            raise e  # Пробрасываем исключение для повторной попытки


    @staticmethod
    @retry(stop=stop_after_delay(3600), wait=wait_exponential(multiplier=1, min=1, max=3600))
    async def complete_transfer(server_address, filename):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{server_address}/complete", params={"filename": filename}) as response:
                    if response.status == 200:
                        logging.info("Transfer completed successfully on server.")
                        return True
                    else:
                        logging.error(f"Server responded with status code {response.status} on transfer completion.")
                        raise Exception(f"Failed to complete transfer, server responded with {response.status}")
        except aiohttp.ClientError as e:
            logging.error(f"Connection error while finalizing transfer: {e}")
            raise e  # Пробрасываем исключение для повторной попытки
