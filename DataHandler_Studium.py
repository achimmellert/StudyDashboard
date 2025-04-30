# DataHandler_Studium.py
import json
from dataclasses import dataclass, asdict
from typing import List, Dict
import os
from file_manager import JSONFileManager

# Basisverzeichnis und Dateipfade, sicherstellen, dass Ordner existiert
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE_DIRECTORY = os.path.join(BASE_DIR, 'data_files')
os.makedirs(JSON_FILE_DIRECTORY, exist_ok=True)

JSON_FILE_NAME = 'studium.json'
JSON_FILE_ABS_PATH = os.path.join(JSON_FILE_DIRECTORY, JSON_FILE_NAME)

GRADE_JSON_PATH = os.path.join(JSON_FILE_DIRECTORY, 'grades.json')


@dataclass
class Module:
    """
    Modul-Klasse, welche nur auf Semesterebene erstellt werden kann.
    """
    name: str = ""
    professor: str = ""
    topics: str = ""
    notes: str = ""
    progress: int = 0  # Fortschritt in Prozent (0–100)
    project: str | None = None
    exam_date: str | None = None
    exam_grade: float = 0.0

    def get_progress(self) -> int:
        return self.progress

    def get_grade(self) -> float:
        return float(self.exam_grade)


class Semester:
    """
    Semester-Klasse. Dient als Objekt-Manager für die dazugehörige Modul-Liste.
    """
    def __init__(self, semester_nr: str):
        self.semester_nr = semester_nr
        self.modules: List[Module] = []

    def add_modul(self, modul: Module) -> None:
        """
        Modul-Objekt der Liste hinzufügen.
        :param modul:
        :return: None
        """
        self.modules.append(modul)

    def get_serialized_modules(self) -> List[Dict]:
        """
        Modul wird serialisiert mithilfe der dataclass-Methode asdict()
        :return: Dict
        """
        return [asdict(m) for m in self.modules]

    def get_semester_progress(self) -> int:
        """
        Berechnet den Semesterfortschritt über alle Module des Semesters hinweg.
        :return: int
        """
        if not self.modules:
            return 0
        total = sum(m.get_progress() for m in self.modules)
        return total // len(self.modules)


class Studies:
    """
    Singleton zur zentralen Verwaltung des Studiums.
    """
    _instance = None # Klassenvariable zur Speicherung der einzigen Instanz

    def __new__(cls):  # Singleton
        if cls._instance is None:
            cls._instance = super(Studies, cls).__new__(cls) # ruft die __new__-Methode von object auf
        return cls._instance

    def __init__(self) -> None:
        """
        Erstellt Semester-Dictionary.
        Holt die gespeicherten Semester-Module aus der JSON und fügt sie dem Dictionary in korrekter Syntax hinzu.
        """
        if not hasattr(self, "semester_dict"):
            self.semester_dict = {str(i): Semester(str(i)) for i in range(1, 7)}
            loaded_data = self._load_from_json()
            for sem, mods in loaded_data.items():
                self.semester_dict[sem].modules = mods  # Liste wird einmal vollständig überschrieben

    def add_modul(self, semester: str, modul: Module):
        self.semester_dict[semester].add_modul(modul)
        self._save_to_json()

    def delete_modul(self, semester: str, module_index: int):
        """
        Löscht ein Modul basierend auf dem Semester und dem Modul-Index aus der Modul-Liste.
        :param semester: str
        :param module_index: int
        :return: None
        """
        if semester in self.semester_dict:
            try:
                del self.semester_dict[semester].modules[module_index]
                self._save_to_json()
            except IndexError:
                print(f"Modul an Index {module_index} existiert nicht.")

    def get_modules_by_semester(self, semester: str) -> List[Dict]:
        return self.semester_dict[semester].get_serialized_modules()

    def get_all_modules(self):
        """
        Holt alle Module, unabhängig vom Semester.
        :return: List[Module]
        """
        all_modules = []
        for sem_obj in self.semester_dict.values():
            all_modules.extend(sem_obj.modules)
        return all_modules

    def get_semester_progress(self, semester: str) -> int:
        return self.semester_dict[semester].get_semester_progress()

    def get_overall_progress(self) -> int:
        """
        Berechnet den Gesamtfortschritt, basierend auf allen eingeschriebenen Modulen.
        :return: int
        """
        overall_modules = 0
        overall_progress = 0
        for sem_obj in self.semester_dict.values():
            for module in sem_obj.modules:
                overall_progress += module.get_progress()
                overall_modules += 1
        if overall_modules == 0:
            return 0
        return (overall_progress * 100) // (overall_modules * 100)

    def get_gpa(self) -> float:
        """
        Berechnet den aktuellen Notendurchschnitt.
        :return: float
        """
        overall_modules_with_full_progress = 0
        sum_grades = 0.0
        for sem_obj in self.semester_dict.values():
            for module in sem_obj.modules:
                if module.get_progress() == 100:
                    overall_modules_with_full_progress += 1
                    sum_grades += module.get_grade()
        if overall_modules_with_full_progress == 0:
            return 0
        return round((sum_grades / overall_modules_with_full_progress), 2)

    def _save_to_json(self) -> None:  # Persistenz
        data = {}
        for sem_nr, sem_obj in self.semester_dict.items():
            data[sem_nr] = sem_obj.get_serialized_modules()
        manager = JSONFileManager(JSON_FILE_ABS_PATH)
        manager.save(data)

    def _load_from_json(self) -> Dict[str, List[Module]]:
        manager = JSONFileManager(JSON_FILE_ABS_PATH)
        data = manager.load()
        if data:
            return {sem: [Module(**m) for m in mods] for sem, mods in data.items()}
        return {str(i): [] for i in range(1, 7)}


class GradeDevelopment:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GradeDevelopment, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "grade_history"):
            self.grade_history = []
            self.update_callback = None  # Speicherung des Callbacks
            self._load_from_json()

    def set_update_callback(self, callback):
        self.update_callback = callback  # Setzung des Callbacks (Plot)

    def update(self):
        """Aktualisiert den Notenverlauf mit dem aktuellen GPA aus Studies."""
        studium = Studies()
        current_gpa = studium.get_gpa()
        if current_gpa == 0:
            return  # Keine Noten vorhanden
        # Zähle die Anzahl der Module mit Noten
        count = int(sum(1 for sem in studium.semester_dict.values() for m in sem.modules if m.exam_grade != 0.0))
        new_entry = {"count": count, "average": current_gpa}
        self.grade_history.append(new_entry)
        self._save_to_json()
        if self.update_callback:
            self.update_callback()  # Aufruf des Callbacks (Plot-Funktion)

    def _save_to_json(self):
        """Speichert den Notenverlauf in grades.json."""
        manager = JSONFileManager(GRADE_JSON_PATH)
        manager.save(self.grade_history)

    def _load_from_json(self):
        """Lädt den Notenverlauf aus grades.json."""
        manager = JSONFileManager(GRADE_JSON_PATH)
        data = manager.load()
        if data:
            self.grade_history = data
        else:
            self.grade_history = []
