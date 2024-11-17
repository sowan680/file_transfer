import json
import os

class StateManager:
    def __init__(self, state_file='transfer_state.json'):
        self.state_file = state_file
        self.sent_chunks = set()
        self._load_state()

    def is_chunk_sent(self, index):
        return index in self.sent_chunks

    def mark_chunk_sent(self, index):
        self.sent_chunks.add(index)
        self._save_state()

    def reset_state(self):
        self.sent_chunks.clear()
        if os.path.exists(self.state_file):
            os.remove(self.state_file)
