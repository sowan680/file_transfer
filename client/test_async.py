import asyncio
import os
import logging
from file_sender import FileSender  # Assuming the above code is saved as file_sender.py

# Set up logging
logging.basicConfig(
    level=logging.INFO,  # Set minimum log level to display
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    handlers=[logging.StreamHandler()]  # Handler for logging to console
)

async def send_file(server_address, filepath):
    sender = FileSender(server_address, filepath)
    await sender.start_transfer()

async def main():
    server_address = "http://localhost:8000"
    files = [
        "tests/test1.exe",
        "tests/test2.exe",
        "tests/test3.exe",
        "tests/test4.docx",
        "tests/test5.docx",
        "tests/test6.docx",
        "tests/test7.docx",
        "tests/test8.docx",
        "tests/test9.docx",
        "tests/test10.docx",
    ]

    # Ensure all files exist before starting
    for filepath in files:
        if not os.path.exists(filepath):
            logging.error(f"File {filepath} does not exist. Please check the path and try again.")
            return

    # Create a list of tasks to send all files concurrently
    tasks = [send_file(server_address, filepath) for filepath in files]
    
    # Run all tasks concurrently
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
