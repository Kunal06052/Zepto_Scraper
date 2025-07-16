# src/utils/checkpoint.py

import os

class CheckpointManager:
    def __init__(self, checkpoint_file="last_checkpoint.txt"):
        self.checkpoint_file = checkpoint_file

    def save(self, subcat_name, index=0):
        """Save progress to file"""
        with open(self.checkpoint_file, "w", encoding="utf-8") as f:
            f.write(f"{subcat_name},{index}")

    def load(self):
        """Load last processed subcategory and index"""
        if not os.path.exists(self.checkpoint_file):
            return None, None
        with open(self.checkpoint_file, "r", encoding="utf-8") as f:
            line = f.read().strip()
            if line:
                parts = line.split(",")
                if len(parts) >= 2:
                    return parts[0], int(parts[1])
                return parts[0], 0
        return None, None