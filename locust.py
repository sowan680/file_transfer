from locust import HttpUser, TaskSet, task, between
import os
import logging
import asyncio
from client.file_sender import FileSender

# Путь к видеофайлу для отправки
VIDEO_PATH = 'client/test1.mp4'

# Конфигурация логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UserBehavior(TaskSet):
    def on_start(self):
        """
        Метод, выполняемый при старте клиента.
        """
        self.server_address = "http://localhost:8000"
        self.file_sender = FileSender(self.server_address, VIDEO_PATH)
        self.loop = asyncio.get_event_loop()

    @task
    def upload_file(self):
        """
        Задача отправки файла с помощью класса FileSender.
        """
        logging.info(f"Starting file upload task for {VIDEO_PATH}.")
        self.loop.create_task(self.file_sender.start_transfer())

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0.1, 1.0)

    def on_start(self):
        logging.info("Locust test user started.")

    def on_stop(self):
        logging.info("Locust test user stopped.")
