# video_blockchain.py

from hashlib import sha256
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, sender, receiver, video_hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.sender = sender
        self.receiver = receiver
        self.video_hash = video_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.sender}{self.receiver}{self.video_hash}"
        return sha256(block_string.encode()).hexdigest()

class VideoBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Creator", "Initial", "video_hash")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, sender, receiver, video_hash):
        latest_block = self.get_latest_block()
        new_block = Block(latest_block.index + 1, latest_block.hash, time.time(), sender, receiver, video_hash)
        self.chain.append(new_block)
        return new_block.hash

def add_to_blockchain(video_path):
    # Placeholder for generating a video hash
    video_hash = "dummy_video_hash"  # Replace with actual hash of the video
    blockchain = VideoBlockchain()
    blockchain.add_block("User1", "User2", video_hash)
    return blockchain.get_latest_block().hash
