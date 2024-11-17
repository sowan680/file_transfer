import asyncio
import pytest
from client.file_sender import FileSender

@pytest.mark.asyncio
async def test_multiple_clients():
    server_address = "http://localhost:8000"
    filepaths = [r"E:\Soft\Wo Xing Shi Meme Furina.mp4",
                 r"E:\Soft\Wo Xing Shi Meme Furina.mp4",
                 r"E:\Soft\Wo Xing Shi Meme Furina.mp4",
                 r"E:\Soft\Wo Xing Shi Meme Furina.mp4",
                 r"E:\Soft\Wo Xing Shi Meme Furina.mp4",
                 r"E:\Soft\Wo Xing Shi Meme Furina.mp4",
                 r"E:\Soft\Wo Xing Shi Meme Furina.mp4",
                 r"E:\Soft\Wo Xing Shi Meme Furina.mp4",
                 r"E:\Soft\Wo Xing Shi Meme Furina.mp4",
                 r"E:\Soft\Wo Xing Shi Meme Furina.mp4"]

    async def send_file(filepath):
        sender = FileSender(server_address, filepath=filepath)
        await sender.start_transfer()

    tasks = [send_file(filepath) for filepath in filepaths]
    await asyncio.gather(*tasks)

    assert True
