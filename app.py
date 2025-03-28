# app.py
import customtkinter as ctk
from visuals.settings import BG_COLOR
from widgets import Notes_Logic, Modules_Semester_Logic, ToDo_Logic, Key_Metrics_Logic, Grade_Development_Logic


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Mein Dashboard fürs Studium')
        self.geometry('1600x1100')
        self.configure(fg_color=BG_COLOR)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)
        self.create_frames()
        self.create_widgets()
        self.place_widgets()
        self.show_toast()

    def create_frames(self):
        self.left_frame = ctk.CTkFrame(self, fg_color='white')
        self.left_frame.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=10, pady=10)
        self.top_frame = ctk.CTkFrame(self, fg_color='white')
        self.top_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        self.bottom_frame = ctk.CTkFrame(self, fg_color='white')
        self.bottom_frame.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)
        self.right_frame = ctk.CTkFrame(self, fg_color='white')
        self.right_frame.grid(row=0, column=2, rowspan=2, sticky='nsew', padx=10, pady=10)

    def create_widgets(self):
        self.notepad = Notes_Logic.NoteApp(self.top_frame)
        self.semester_progress = Modules_Semester_Logic.SemesterProgressApp(self.top_frame)
        self.to_do = ToDo_Logic.ToDoApp(self.left_frame)
        self.key_metrics = Key_Metrics_Logic.KeyMetricsApp(self.right_frame)
        self.grade_development = Grade_Development_Logic.GradeDevelopmentApp(self.bottom_frame)

    def place_widgets(self):
        self.notepad.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        self.semester_progress.pack(side='right', expand=True, fill='both', padx=5, pady=5)
        self.to_do.pack(expand=True, fill='both', padx=5, pady=5)
        self.key_metrics.pack(expand=True, fill='both', padx=5, pady=5)
        self.grade_development.pack(expand=True, fill='both', padx=20, pady=20)

    def show_toast(self):
        Toast(self)


class Toast(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('')
        self.resizable(False, False)
        self.overrideredirect(True)
        message = 'Willkommen 👾'
        label = ctk.CTkLabel(self, text=message, text_color="white", corner_radius=20, bg_color='#19233c', font=('Arial', 50, 'bold'))
        label.pack(expand=True, fill="both", padx=10, pady=10)
        self.lift()
        self.attributes("-topmost", True)
        self.after(3000, self.destroy)
