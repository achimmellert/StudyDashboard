# Modules_Semester_Logic.py
import customtkinter as ctk
import tkinter as tk
from DataHandler_Studium import Studies, Module, GradeDevelopment
from visuals.settings import BG_COLOR, BORDER_COLOR, HEADER_BG_COLOR


class Calendar(ctk.CTkToplevel):
    """
    Da Customtkinter keinen eingebauten Kalender besitzt, wird er hiermit manuell erstellt.
    Wird automatisch geöffnet, wenn im ModuleSettingsWindow das Klausur-Datum eingestellt werden soll.
    """
    def __init__(self, master, callback, initial_date=None):
        super().__init__(master)
        self.callback = callback
        self.title("Datum wählen")
        self.geometry("250x150")
        self.resizable(False, False)
        label_day = ctk.CTkLabel(self, text="Tag:")
        label_day.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.spin_day = tk.Spinbox(self, from_=1, to=31, width=5, font=("Arial", 12))
        self.spin_day.grid(row=0, column=1, padx=5, pady=5)
        label_month = ctk.CTkLabel(self, text="Monat:")
        label_month.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.spin_month = tk.Spinbox(self, from_=1, to=12, width=5, font=("Arial", 12))
        self.spin_month.grid(row=1, column=1, padx=5, pady=5)
        label_year = ctk.CTkLabel(self, text="Jahr:")
        label_year.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.spin_year = tk.Spinbox(self, from_=2025, to=2100, width=5, font=("Arial", 12))
        self.spin_year.grid(row=2, column=1, padx=5, pady=5)
        if initial_date:
            try:
                year, month, day = map(int, initial_date.split("-"))
                self.spin_year.delete(0, "end")
                self.spin_year.insert(0, str(year))
                self.spin_month.delete(0, "end")
                self.spin_month.insert(0, str(month))
                self.spin_day.delete(0, "end")
                self.spin_day.insert(0, str(day))
            except Exception:
                pass
        self.ok_button = ctk.CTkButton(self, text="OK", command=self.on_ok)
        self.ok_button.grid(row=3, column=0, columnspan=2, pady=10)
        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))

    def on_ok(self):
        day = int(self.spin_day.get())
        month = int(self.spin_month.get())
        year = int(self.spin_year.get())
        formatted_date = f"{year:04d}-{month:02d}-{day:02d}"
        self.callback(formatted_date)
        self.destroy()


class ModuleSettingsWindow(ctk.CTkToplevel):
    """
    TopLevel-Fenster, welches sich öffnet, sobald die Einstellungen/Attribute eines Moduls festgelegt werden sollen.
    Da in Tkinter üblich, werden die Widgets direkt in der init-Methode initialisiert.
    """
    def __init__(self, semester_nr: str, module_index: int, modul: Module):
        super().__init__()
        self.semester_nr = semester_nr
        self.module_index = module_index
        self.modul = modul
        self.title(f"Moduleinstellungen: {modul.name}")
        self.resizable(False, False)

        # Festlegung der Tkinter-Variablen zur internen Speicherung
        self.name_var = tk.StringVar(value=modul.name)
        self.professor_var = tk.StringVar(value=modul.professor)
        self.topics_var = tk.StringVar(value=modul.topics)
        self.notes_var = tk.StringVar(value=modul.notes)
        self.progress_var = tk.IntVar(value=modul.progress)
        self.project_var = tk.StringVar(value=modul.project if modul.project else "")
        self.exam_date_var = tk.StringVar(value=modul.exam_date if modul.exam_date else "")
        self.exam_grade_var = tk.StringVar(value=str(modul.exam_grade) if modul.exam_grade else "")
        padding = 10

        # Konfiguration der einzelnen Widgets
        self.name_label = ctk.CTkLabel(self, text="Modulname:")
        self.name_label.pack(padx=padding, pady=(padding, 0), anchor="w")
        self.name_entry = ctk.CTkEntry(self, textvariable=self.name_var)
        self.name_entry.pack(padx=padding, pady=(0, padding), fill="x")
        self.prof_label = ctk.CTkLabel(self, text="Professor:")
        self.prof_label.pack(padx=padding, pady=(padding, 0), anchor="w")
        self.prof_entry = ctk.CTkEntry(self, textvariable=self.professor_var)
        self.prof_entry.pack(padx=padding, pady=(0, padding), fill="x")
        self.topics_label = ctk.CTkLabel(self, text='Themen')
        self.topics_label.pack(padx=padding, pady=(padding, 0), anchor="w")
        self.topics_textbox = ctk.CTkTextbox(self, height=100)
        self.topics_textbox.pack(padx=padding, pady=(0, padding), fill="x")
        self.topics_textbox.insert('1.0', self.topics_var.get())
        self.notes_label = ctk.CTkLabel(self, text="Notizen:")
        self.notes_label.pack(padx=padding, pady=(padding, 0), anchor="w")
        self.notes_entry = ctk.CTkEntry(self, textvariable=self.notes_var)
        self.notes_entry.pack(padx=padding, pady=(0, padding), fill="x")
        self.progress_label = ctk.CTkLabel(self, text="Fortschritt (0-100):")
        self.progress_label.pack(padx=padding, pady=(padding, 0), anchor="w")
        self.progress_slider = ctk.CTkSlider(self, from_=0, to=100, variable=self.progress_var, command=self.check_slider)
        self.progress_slider.pack(padx=padding, pady=(0, padding), fill="x")
        self.project_label = ctk.CTkLabel(self, text="Projekt (falls vorhanden):")
        self.project_label.pack(padx=padding, pady=(padding, 0), anchor="w")
        self.project_entry = ctk.CTkEntry(self, textvariable=self.project_var)
        self.project_entry.pack(padx=padding, pady=(0, padding), fill="x")
        self.exam_label = ctk.CTkLabel(self, text="Prüfungstermin (yyyy-mm-dd):")
        self.exam_label.pack(padx=padding, pady=(padding, 0), anchor="w")
        self.date_frame = ctk.CTkFrame(self)
        self.date_frame.pack(padx=padding, pady=(0, padding), fill="x")
        self.exam_entry = ctk.CTkEntry(self.date_frame, textvariable=self.exam_date_var, state='disabled')
        self.exam_entry.pack(side="left", expand=True, fill="x")
        self.date_button = ctk.CTkButton(self.date_frame, text="Datum wählen", command=self.open_calendar)
        self.date_button.pack(side="right", padx=(padding, 0))
        self.exam_grade_label = ctk.CTkLabel(self, text='Note:')
        self.exam_grade_label.pack(padx=padding, pady=(padding, 0), anchor="w")
        self.exam_grade_entry = ctk.CTkEntry(self, textvariable=self.exam_grade_var, state='disabled')
        self.exam_grade_entry.pack(padx=padding, pady=(0, padding), fill="x")
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(padx=padding, pady=padding, fill="x")
        self.save_button = ctk.CTkButton(self.button_frame, text="Speichern", command=self.save_changes)
        self.save_button.pack(side="left", padx=(0, padding))
        self.cancel_button = ctk.CTkButton(self.button_frame, text="Abbrechen", command=self.destroy)
        self.cancel_button.pack(side="right", padx=(padding, 0))
        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))

    def check_slider(self, value):
        if int(float(value)) == 100:
            self.exam_grade_entry.configure(state='normal')

    def open_calendar(self):
        """
        Öffnet Kalender, sofern Klausurdatum geklickt wurde.
        :return: None
        """
        def on_date_selected(selected_date):
            self.exam_date_var.set(selected_date)
        Calendar(self, callback=on_date_selected, initial_date=self.exam_date_var.get())

    def save_changes(self):
        """
        Holt die Daten aus den einzelnen Tkinter-Variablen und speichert diese direkt in die zugehörigen Modul-Attribute
        Außerdem werden die Änderungen ebenfalls direkt in die JSON-Datei gespeichert.
        :return: None
        """
        self.modul.name = self.name_var.get()
        self.modul.professor = self.professor_var.get()
        self.modul.topics = self.topics_textbox.get('1.0', 'end-1c')
        self.modul.notes = self.notes_var.get()
        self.modul.progress = self.progress_var.get()
        self.modul.project = self.project_var.get() if self.project_var.get() != "" else None
        self.modul.exam_date = self.exam_date_var.get() if self.exam_date_var.get() != "" else None
        self.modul.exam_grade = float(self.exam_grade_var.get()) if self.exam_grade_var.get() != "" else 0.0
        Studies()._save_to_json()
        # Nur update() aufrufen, wenn eine Note gesetzt wurde
        if self.modul.exam_grade != 0.0:
            GradeDevelopment().update()  # Kein Parameter, da update() den GPA selbst holt
        self.destroy()


class ModuleOverviewWindow(ctk.CTkToplevel):
    """
    Weiteres TopLevel-Fenster, welches geöffnet wird, um alle Module eines Seemsters anzeigen zu lassen.
    """
    def __init__(self, semester_nr: str):
        super().__init__()
        self.semester_nr = semester_nr
        self.title(f"Module für Semester {semester_nr}")
        self.geometry("500x500")
        self.resizable(False, False)
        self.studium = Studies()
        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))
        self.module_frame = ctk.CTkFrame(self)
        self.module_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.new_module_frame = ctk.CTkFrame(self)
        self.new_module_frame.pack(fill="x", padx=10, pady=5)
        self.new_module_entry = ctk.CTkEntry(self.new_module_frame, placeholder_text="Neuer Modulname")
        self.new_module_entry.pack(side="left", expand=True, fill="x", padx=5, pady=5)
        self.add_module_button = ctk.CTkButton(self.new_module_frame, text="+", command=self.add_module)
        self.add_module_button.pack(side="left", padx=5, pady=5)
        self.buttons = []
        self.refresh_module_buttons()

    def refresh_module_buttons(self):
        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()
        modules = self.studium.get_modules_by_semester(self.semester_nr)
        for idx, module in enumerate(modules):
            btn = ctk.CTkButton(
                self.module_frame,
                text=module["name"],
                command=lambda i=idx: self.open_module_settings(i)
            )
            btn.pack(fill="x", padx=5, pady=5)
            btn.bind("<Button-3>", lambda event, i=idx: self.open_delete_window(i))
            self.buttons.append(btn)

    def add_module(self):
        modulename = self.new_module_entry.get().strip()
        if modulename:
            new_module = Module(name=modulename)
            self.studium.add_modul(self.semester_nr, new_module)
            self.new_module_entry.delete(0, tk.END)
            self.refresh_module_buttons()

    def open_module_settings(self, module_index: int):
        module_list = self.studium.semester_dict[self.semester_nr].modules
        module_obj = module_list[module_index]
        ModuleSettingsWindow(self.semester_nr, module_index, module_obj)

    def open_delete_window(self, module_index: int):
        ModuleDeleteWindow(self, self.semester_nr, module_index)

class ModuleDeleteWindow(ctk.CTkToplevel):
    """
    TopLevel-Fenster zur Abfrage zur tatsächlichen Löschung eines Moduls.
    """
    def __init__(self, parent, semester_nr: str, module_index: int):
        super().__init__(parent)
        self.parent = parent
        self.semester_nr = semester_nr
        self.module_index = module_index
        self.studium = Studies()
        self.title("Module löschen?")
        self.geometry("300x150")
        self.resizable(False, False)
        module_list = self.studium.semester_dict[self.semester_nr].modules
        self.module_name = module_list[module_index].name if module_list else "Unbekannt"
        label = ctk.CTkLabel(self, text=f"Möchtest du '{self.module_name}' wirklich löschen?")
        label.pack(pady=10, padx=10)
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=10, pady=10)
        confirm_button = ctk.CTkButton(button_frame, text="Ja, löschen", command=self.delete_module)
        confirm_button.pack(side="left", expand=True, fill="x", padx=5)
        cancel_button = ctk.CTkButton(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side="right", expand=True, fill="x", padx=5)
        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))

    def delete_module(self):
        self.studium.delete_modul(self.semester_nr, self.module_index)
        self.parent.refresh_module_buttons()
        import tkinter.messagebox as messagebox
        messagebox.showinfo("Erfolg", f"Module '{self.module_name}' wurde gelöscht.")
        self.destroy()


class SemesterProgressApp(ctk.CTkFrame):
    """
    Übergeordnetes Frame, welches das eigentliche Übersichtsfenster der Semester in der App anzeigt.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color=BG_COLOR)
        self.studium = Studies()
        self.header = ctk.CTkLabel(
            self,
            corner_radius=10,
            anchor='center',
            height=50,
            text='Semesterfortschritt',
            text_color='white',
            font=('Arial', 30, 'bold')
        )
        self.header.pack(side='top', fill='both', pady=10, padx=10)
        self.semester_buttons = []
        self.progress_labels = []
        self.progress_bars = []
        frame_opts = {
            'master': self,
            'corner_radius': 10,
            'border_color': BORDER_COLOR,
            'fg_color': BG_COLOR
        }
        for i in range(1, 7):
            sem_frame = ctk.CTkFrame(**frame_opts)
            sem_frame.pack(side='top', fill='x', pady=5, padx=10)
            sem_label = ctk.CTkButton(
                sem_frame,
                text=f"Semester {i}",
                fg_color=BG_COLOR,
                font=('Arial', 20),
                command=lambda sem=i: self.open_module_window(str(sem))
            )
            sem_label.pack(side='left', fill='both', expand=True, pady=10, padx=5)
            self.semester_buttons.append(sem_label)
            prog = self.studium.get_semester_progress(str(i))
            progress_label = ctk.CTkLabel(sem_frame, text=f"{prog}%", font=('Arial', 15, 'bold'), width=50, text_color='white')
            progress_label.pack(side='right', padx=(0, 10), pady=5)
            self.progress_labels.append(progress_label)
            prog_bar = ctk.CTkProgressBar(sem_frame, width=100)
            prog_bar.pack(side='right', padx=(0, 10), pady=5)
            prog_bar.set(prog / 100)
            self.progress_bars.append(prog_bar)
        self.overall_frame = ctk.CTkFrame(self, corner_radius=30, fg_color=BG_COLOR)
        self.overall_frame.pack(side='bottom', expand=True, fill='both', padx=10, pady=10)
        self.overall_label = ctk.CTkLabel(self.overall_frame, text="Gesamtfortschritt:", fg_color=BG_COLOR, font=('Arial', 20), text_color='white')
        self.overall_label.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        overall_prog = self.studium.get_overall_progress()
        self.overall_progress_label = ctk.CTkLabel(self.overall_frame, text=f"{overall_prog}%", fg_color=BG_COLOR, font=('Arial', 20),text_color='white')
        self.overall_progress_label.pack(side='right', expand=True, fill='both', padx=5, pady=5)
        self.after(2000, self.update_progress)

    def update_progress(self):
        for i in range(1, 7):
            prog = self.studium.get_semester_progress(str(i))
            self.progress_labels[i - 1].configure(text=f"{prog}%")
            self.progress_bars[i - 1].set(prog / 100)
        overall_prog = self.studium.get_overall_progress()
        self.overall_progress_label.configure(text=f"{overall_prog}%")
        self.after(2000, self.update_progress)

    def open_module_window(self, semester_nr: str):
        ModuleOverviewWindow(semester_nr)
