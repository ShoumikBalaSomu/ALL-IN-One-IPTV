import os

class FolderManager:
    @staticmethod
    def create_output_structure(base_dir: str):
        os.makedirs(os.path.join(base_dir, "output"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "input"), exist_ok=True)
