# DataHandler_Studium.py
import json
from dataclasses import dataclass, asdict
from typing import List, Dict
import os
from file_manager import JSONFileManager

# Basisverzeichnis und Dateipfade
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE_DIRECTORY = os.path.join(BASE_DIR, 'data_files')
os.makedirs(JSON_FILE_DIRECTORY, exist_ok=True)

JSON_FILE_NAME = 'studium.json'
JSON_FILE_ABS_PATH = os.path.join(JSON_FILE_DIRECTORY, JSON_FILE_NAME)

GRADE_JSON_PATH = os.path.join(JSON_FILE_DIRECTORY, 'grades.json')


@dataclass
class Module:
    name: str = ""
    professor: str = ""
    topics: str = ""
    notes: str = ""
    progress: int = 0  # Fortschritt in Prozent (0–100)
    project: str | None = None
    exam_date: str | None = None
    exam_grade: float = 0.0
    