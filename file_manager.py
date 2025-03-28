# file_manager.py
import os
import json


class JSONFileManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    return None
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def save(self, data):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)


class TextFileManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def load(self) -> str:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            return ""

    def save(self, text: str):
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(text)
