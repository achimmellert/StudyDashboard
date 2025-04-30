# file_manager.py
import os
import json


class JSONFileManager:
    """
    Lädt und speichert JSON-Dateien.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def load(self):
        """
        Lädt den Inhalt aus einer JSON heraus und gibt ihn als Dictionary zurück.
        :return: dict
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    return None
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def save(self, data):
        """
        Speichert das Dictionary als JSON. Das Dictionary muss dabei im korrekten JSON-Format vorliegen.
        :param data: Dict
        :return: None
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


class TextFileManager:
    """
    Lädt und speichert Text-Dateien.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def load(self) -> str:
        """
        Lädt den Inhalt aus einer txt heraus und gibt ihn als String zurück.
        :return: str
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            return ""

    def save(self, text: str):
        """
        Speichert den String im angegeben Pfad.
        :param text: str
        :return: None
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(text)
