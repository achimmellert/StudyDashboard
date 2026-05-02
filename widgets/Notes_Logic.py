import customtkinter as ctk
import os
from visuals.settings import BG_COLOR


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Verzeichnis von Notes_Logic.py
PARENT_DIR = os.path.dirname(SCRIPT_DIR)  # Eine Ebene höher
FILE_DIRECTORY = os.path.join(PARENT_DIR, 'storage')  # storage im übergeordneten Ordner
os.makedirs(FILE_DIRECTORY, exist_ok=True)  # Erstellt den Ordner, falls er nicht existiert


def get_file_path(tab):
    filename = f"tab{tab}.txt"
    return os.path.join(FILE_DIRECTORY, filename)


class NoteApp(ctk.CTkFrame):
    """
    Definiert den Aufbau des Notiz-Widgets in der App.
    """
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=BG_COLOR)

        self.header = ctk.CTkLabel(self, corner_radius=10, anchor='center', height=50, text=' Allgemeine Notizen',
                                   font=('Arial', 30, 'bold'), text_color='white')
        self.header.pack(side='top', fill='both', pady=10, padx=10)

        self.notebook = ctk.CTkTabview(self, fg_color='transparent')
        self.notebook.pack(expand=True, fill="both")

        # Besteht aus 2 Tabs.
        self.notebook.add("Tab 1")
        self.notebook.add("Tab 2")
        self.tab1 = Tab(self.notebook.tab("Tab 1"), get_file_path(1), 'Tab 1')
        self.tab2 = Tab(self.notebook.tab("Tab 2"), get_file_path(2), 'Tab 2')
        self.tab1.pack(expand=True, fill="both")
        self.tab2.pack(expand=True, fill="both")


class Tab(ctk.CTkFrame):
    """
    Klasse für jedes der beiden Tabs aus der Notiz-App. Entspricht jeweils einer einfachen Tkinter-Textbox.
    """
    def __init__(self, parent, file_path, note_title):
        super().__init__(master=parent, fg_color=BG_COLOR)

        self.file_path = file_path
        self.textbox = ctk.CTkTextbox(self, font=('Arial', 20), wrap='word')
        self.textbox.pack(expand=True, fill='both', padx=5, pady=5)
        self.textbox.bind('<<Modified>>', self.auto_save)

        self.load_note()


    def auto_save(self, event=None):
        """
        Sobald Änderungen vorgenommen werden im Textfeld, werden diese automatisch und sofort gespeichert.
        :param event:
        :return: None
        """
        if self.textbox.edit_modified():
            text = self.textbox.get("1.0", "end").strip()
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write(text)
            self.textbox.edit_modified(False)


    def load_note(self):

        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                text = file.read()
                self.textbox.insert("1.0", text)
