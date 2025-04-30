# ToDo_Logic.py
import customtkinter as ctk
import tkinter as tk
from CTkMessagebox import CTkMessagebox
from DataHandler_Studium import Studies
from DataHandler_ToDos_LearnStreak import ToDoList, ToDo
from visuals.settings import BG_COLOR

class ToDoApp(ctk.CTkFrame):
    """
    Definiert den Aufbau des To-Do-Widgets in der App.
    """
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=BG_COLOR)
        self.studium = Studies() # Studies-Instanz für dessen Methoden
        self.todos = ToDoList() # ToDoList-Instanz für dessen Methoden

        # Konfiguration der Widgets
        self.header = ctk.CTkLabel(
            self,
            corner_radius=10,
            anchor='center',
            height=50,
            text="Heutige To Do's",
            text_color='white',
            font=('Arial', 30, 'bold')
        )
        self.header.pack(side='top', fill='both', pady=10, padx=10)
        self.todos_frame = ctk.CTkFrame(self)
        self.todos_frame.pack(expand=True, fill='both')
        self.todo_widgets = []
        self.place_todos()
        self.button_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.button_frame.pack(side='bottom', pady=10)
        self.button = ctk.CTkButton(
            self.button_frame, text='Neues To-Do hinzufügen', font=('Arial', 15), command=self.create_add_todo_window, corner_radius=10)
        self.button.pack()

    def create_add_todo_window(self):
        AddToDoWindow(self, self.studium)

    def save_new_todo(self, description, module, time, is_done=False):
        """
        Speichert das neue To-Do ab.
        """
        new_todo = ToDo(description, module, time, is_done)
        self.todos.add_todo(new_todo) # ToDo-Klasse sorgt auch direkt für dauerhafte Speicherung als JSON.
        self.refresh_todos()
        CTkMessagebox(title='Info', message='Neues To-Do erfolgreich gespeichert', icon='info')

    def delete_todo(self, todo: ToDo):
        self.todos.remove_todo(todo.description)
        self.refresh_todos()
        CTkMessagebox(title='Info', message='To-Do wurde gelöscht', icon='info')

    def refresh_todos(self):
        self.place_todos()

    def place_todos(self):
        """
        Platziert alle To-Dos im Frame in einer ansprechenden Form.
        :return: None
        """
        for widget in self.todo_widgets:
            widget.destroy()
        self.todo_widgets = []
        todos = self.todos.load_from_json()
        for todo in todos:
            frame = ctk.CTkFrame(self.todos_frame)
            frame.pack(fill='x', pady=2, padx=5)
            label = ctk.CTkLabel(
                frame,
                text=f'{todo.description}    |    {todo.module}    |    Zeit: {todo.time}h',
                anchor='w'
            )
            label.pack(side='left', padx=10, fill='x', expand=True)
            delete_btn = ctk.CTkButton(
                frame, text='✅', width=60, font=('Arial', 20),
                command=lambda t=todo: self.delete_todo(t)
            )
            delete_btn.pack(side='right', padx=10)
            self.todo_widgets.append(frame)


class AddToDoWindow(ctk.CTkToplevel):
    """
    Fenster, welches sich öffnet, wenn man ein neues To-Do hinzufügen möchte.
    """
    def __init__(self, todoapp: ToDoApp, studium: Studies):
        super().__init__()
        self.todoapp = todoapp
        self.studium = studium

        # Konfiguration des Frames
        self.geometry('400x300')
        self.title('Neues To-Do hinzufügen')
        self.resizable(False, False)
        self.overrideredirect(True)

        # Tkinter-Variablen
        self.description_var = tk.StringVar()
        self.module_var = tk.StringVar()
        self.time_var = tk.StringVar()
        module_names = [module.name for module in self.studium.get_all_modules()]

        # Konfiguration der Widgets
        ctk.CTkLabel(self, text='Beschreibung:').pack(pady=(10, 0))
        self.description_entry = ctk.CTkEntry(self, textvariable=self.description_var)
        self.description_entry.pack(fill='x', padx=10)
        ctk.CTkLabel(self, text='Module auswählen:').pack(pady=(10, 0))
        self.module_selection = ctk.CTkComboBox(self, values=module_names, variable=self.module_var)
        self.module_selection.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(self, text='Zeit in Stunden:').pack(pady=(10, 0))
        self.time_entry = ctk.CTkEntry(self, textvariable=self.time_var)
        self.time_entry.pack(fill='x', padx=10, pady=5)
        save_button = ctk.CTkButton(
            self,
            text='Speichern',
            command=self.save_todo
        )
        save_button.pack(side='bottom', pady=15)

    def save_todo(self):
        """
        Speichert das eingegebene To-Do ab und löscht die Einträge.
        :return: None
        """
        description = self.description_var.get()
        module = self.module_var.get()
        time = self.time_var.get()
        if description and module and time:
            try:
                time_float = float(time)
                self.todoapp.save_new_todo(description, module, time_float)
                if self.winfo_exists():
                    self.destroy()
            except ValueError:
                CTkMessagebox(title='Fehler', message='Bitte gültige Zeit eingeben', icon='warning')
        else:
            CTkMessagebox(title='Fehler', message='Bitte alle Felder ausfüllen', icon='warning')
