# DataHandler_ToDos_LernStreak.py
from dataclasses import dataclass, asdict
import os
from typing import List
from file_manager import JSONFileManager, TextFileManager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE_DIRECTORY = os.path.join(BASE_DIR, 'data_files')
os.makedirs(JSON_FILE_DIRECTORY, exist_ok=True)
JSON_FILE_NAME = 'todos.json'
JSON_FILE_ABS_PATH = os.path.join(JSON_FILE_DIRECTORY, JSON_FILE_NAME)


@dataclass
class ToDo:
    description: str
    module: str
    time: str
    is_done: bool
    
