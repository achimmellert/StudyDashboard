import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from DataHandler_Studium import GradeDevelopment
from visuals.settings import BG_COLOR


class GradeDevelopmentApp(ctk.CTkFrame):
    """
    Definiert den Aufbau des Notenverlaufs-Widgets als Liniendiagramm in der App.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.grade_dev = GradeDevelopment()
        # Registriere den Callback, damit das Diagramm bei Notenänderungen automatisch aktualisiert wird
        self.grade_dev.set_update_callback(self.plot_grade_development)
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.plot_grade_development()

    def create_widgets(self):
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def plot_grade_development(self):
        """
        Plotten des Diagramms zum Notenverlauf mithilfe von FigureCanvasTkAgg
        :return: None
        """
        data = self.grade_dev.grade_history
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        if not data:
            ctk.CTkLabel(self.graph_frame, text="Noch keine Noten vorhanden.").pack(pady=10)
            return
        counts = [entry["count"] for entry in data]  # Ganze Zahlen (Anzahl benoteter Module)
        averages = [entry["average"] for entry in data]  # Durchschnittsnoten
        fig = Figure(figsize=(6, 4), dpi=100)
        fig.patch.set_facecolor(BG_COLOR)
        ax = fig.add_subplot(111)
        ax.plot(counts, averages, marker='o', linestyle='-', linewidth=2, color='white')
        ax.set_title("Notenentwicklung über Module")
        ax.set_xlabel("Anzahl benoteter Module")
        ax.set_ylabel("Durchschnittsnote")
        ax.set_ylim(5, 1)
        ax.grid(True)
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.set_facecolor(BG_COLOR)
        for spine in ax.spines.values():
            spine.set_color('none')

        ax.set_xticks(counts)
        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
