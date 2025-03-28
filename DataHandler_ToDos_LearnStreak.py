# DataHandler_ToDos_LearnStreak.py
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


class ToDoList:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToDoList, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.todos: List[ToDo] = self.load_from_json()

    def add_todo(self, todo: ToDo):
        self.todos.append(todo)
        self.save_to_json()

    def remove_todo(self, description):
        self.todos = [todo for todo in self.todos if todo.description != description]
        self.save_to_json()

    def save_to_json(self):
        manager = JSONFileManager(JSON_FILE_ABS_PATH)
        data = [asdict(todo) for todo in self.todos]
        manager.save(data)

    def load_from_json(self):
        manager = JSONFileManager(JSON_FILE_ABS_PATH)
        data = manager.load()
        if data:
            return [ToDo(**todo_dict) for todo_dict in data]
        return []


FILE_DIRECTORY = 'data_files'
os.makedirs(FILE_DIRECTORY, exist_ok=True)
FILE_NAME = 'learn_streak.txt'
ABSOLUTE_FILE_PATH = os.path.abspath(os.path.join(FILE_DIRECTORY, FILE_NAME))


class LearnStreak:
    def __init__(self):
        self.learn_streak = self.get_learn_streak()

    def get_learn_streak(self):
        manager = TextFileManager(ABSOLUTE_FILE_PATH)
        content = manager.load()
        try:
            return int(content) if content else 0
        except ValueError:
            print(f"Warnung: Ungültiger Inhalt in {ABSOLUTE_FILE_PATH}. Setze Streak auf 0.")
            return 0

    def increase(self):
        self.learn_streak += 1
        self.save_learn_streak()

    def save_learn_streak(self):
        manager = TextFileManager(ABSOLUTE_FILE_PATH)
        manager.save(str(self.learn_streak))

    def reset(self):
        self.learn_streak = 0
        self.save_learn_streak()
