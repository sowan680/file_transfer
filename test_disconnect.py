import httpx
import os
from client.chunk_manager import ChunkManager
from client.state_manager import StateManager
from client.network_module import NetworkModule
from client.file_sender import FileSender
import pytest

@pytest.mark.asyncio
async def test_file_transfer_with_interruption():
    server_address = "http://localhost:8000"
    filepath = "E:\Soft\Wo Xing Shi Meme Furina.mp4"  # Предполагаем, что существует тестовый файл с этим именем
    chunk_manager = ChunkManager(filepath)
    state_manager = StateManager()

    # Создаем отправителя файла и загружаем половину чанков
    sender = FileSender(server_address)
    sender.filepath = filepath
    sender.chunk_manager = chunk_manager
    sender.state_manager = state_manager
    total_chunks = chunk_manager.total_chunks

    # Отправляем половину чанков
    half_chunks = total_chunks // 2
    for index in range(half_chunks):
        chunk = chunk_manager.get_chunk(index)
        await NetworkModule.send_chunk(server_address, chunk, index, os.path.basename(filepath))
        state_manager.mark_chunk_sent(index)

    # Прерываем передачу (имитация разрыва связи)
    del sender

    # Повторная отправка с того же места
    sender = FileSender(server_address)
    sender.filepath = filepath
    sender.chunk_manager = chunk_manager
    sender.state_manager = state_manager

    # Продолжение загрузки оставшихся чанков
    for index in range(half_chunks, total_chunks):
        if not state_manager.is_chunk_sent(index):
            chunk = chunk_manager.get_chunk(index)
            await NetworkModule.send_chunk(server_address, chunk, index, os.path.basename(filepath))
            state_manager.mark_chunk_sent(index)

    # Завершаем загрузку
    await NetworkModule.complete_transfer(server_address, os.path.basename(filepath))

    # Проверка, что все чанки были отправлены
    assert all(state_manager.is_chunk_sent(index) for index in range(total_chunks))
