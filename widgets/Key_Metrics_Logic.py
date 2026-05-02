import os.path
import customtkinter as ctk
from DataHandler_Studium import Studies
from visuals.settings import BG_COLOR, BORDER_COLOR, HEADER_BG_COLOR
from DataHandler_ToDos_LearnStreak import LearnStreak

FILE_DIRECTORY = '../storage'
os.makedirs(FILE_DIRECTORY, exist_ok=True)
FILE_NAME = 'learn_streak.txt'
ABSOLUTE_FILE_PATH = os.path.abspath(os.path.join(FILE_DIRECTORY, FILE_NAME))


class KeyMetricsApp(ctk.CTkFrame):
    """
    Definiert den Aufbau des Kennzahlen-Widgets in der App.
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_COLOR)
        self.studium = Studies()
        self.lern_streak_manager = LearnStreak()  # Neue Instanz von LernStreak
        self.gpa = self.studium.get_gpa()
        self.lern_streak = self.lern_streak_manager.learn_streak  # Zugriff auf den Wert

        # Konfiguration der Widgets
        self.header = ctk.CTkLabel(
            self,
            text="Kennzahlen",
            font=('Arial', 30, 'bold'),
            fg_color=BG_COLOR,
            text_color='white',
            corner_radius=10,
            height=50
        )
        self.header.pack(side='top', fill='both', pady=10, padx=10)
        self.place_widgets()
        self.bottom_frame = ctk.CTkFrame(self, height=50, fg_color='transparent')
        self.bottom_frame.pack(side='bottom', padx=5, pady=10)
        self.learn_streak_button = ctk.CTkButton(
            self.bottom_frame,
            text="Lern-Streak erhöhen",
            text_color='white',
            font=('Arial', 15),
            corner_radius=10,
            command=self.increase  # Ruft jetzt die Methode der neuen Klasse
        )
        self.learn_streak_button.pack(padx=5, pady=5, expand=True, fill='both')

        self.reset_streak_button = ctk.CTkButton(
            self.bottom_frame,
            text="Lern-Streak zurücksetzen",
            text_color='white',
            font=('Arial', 15),
            corner_radius=10,
            command=self.reset_streak  # Neue Methode
        )
        self.reset_streak_button.pack(side='right', padx=5, pady=5, expand=True, fill='both')

        self.after(2000, self.auto_update) # Aktualisiert sich alle 2 Sekunden.

    def place_widgets(self):
        """
        Platziert die Widgets auf dem Grid.
        :return: None
        """
        widget_frame = ctk.CTkFrame(self)
        widget_frame.pack(expand=True, fill='both', padx=10, pady=10)
        self.gpa_widget = KeyMetricWidget(widget_frame, 'GPA:', self.gpa)
        self.gpa_widget.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.learn_streak_widget = KeyMetricWidget(widget_frame, 'Learn Streak:', self.lern_streak)
        self.learn_streak_widget.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        widget_frame.columnconfigure(0, weight=1)

    def increase(self):
        """
        Erhöht den Lern-Streak, indem dieselbe Methode des Manager-Objekts aufgerufen wird. Das Widget ebenfalls.
        :return:
        """
        self.lern_streak_manager.increase()  # Aufruf der Methode von LernStreak
        self.lern_streak = self.lern_streak_manager.learn_streak  # Wert aktualisieren
        self.learn_streak_widget.update_value(self.lern_streak)

    def reset_streak(self):
        self.lern_streak_manager.reset()  # Setzt den Wert in LernStreak zurück
        self.lern_streak = self.lern_streak_manager.learn_streak  # Aktualisiert den lokalen Wert
        self.learn_streak_widget.reset()  # Setzt das Widget zurück

    def auto_update(self):
        """
        Aktualisiert alle 2 Sekunden den aktuellen GPA.
        :return:
        """
        new_gpa = self.studium.get_gpa()
        if new_gpa != self.gpa:
            self.gpa = new_gpa
            self.gpa_widget.update_value(self.gpa)
        self.after(2000, self.auto_update)


class KeyMetricWidget(ctk.CTkFrame):
    """
    Damit jedes Widget in der Kennzahlen-App identisch aussieht, definiert diese Klasse deren Aussehen.
    """
    def __init__(self, parent, label_name, value):
        super().__init__(parent, fg_color=BG_COLOR, corner_radius=10, border_width=2, border_color=BORDER_COLOR)
        self.value = value
        self.name_label = ctk.CTkLabel(
            self,
            text=label_name,
            text_color=BG_COLOR,
            font=('Arial', 20, 'bold'),
            corner_radius=10,
            fg_color=HEADER_BG_COLOR
        )
        self.name_label.pack(side='left', expand=True, fill='both', padx=10, pady=10)
        self.value_label = ctk.CTkLabel(
            self,
            text=str(value),
            text_color=BG_COLOR,
            font=('Arial', 20, 'bold'),
            corner_radius=10,
            fg_color=HEADER_BG_COLOR
        )
        self.value_label.pack(side='right', expand=True, fill='both', padx=10, pady=10)

    def update_value(self, new_value):
        self.value = new_value
        self.value_label.configure(text=str(new_value))

    def reset(self):
        self.value = 0
        self.value_label.configure(text='0')