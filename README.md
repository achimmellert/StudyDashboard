# Study Dashboard

A Python-based desktop application for students to manage and track their university progress. Built with `customtkinter`.

## Features

- **Semester & Module Management**: Organize your modules by semester. Keep track of professors, topics, and notes.
- **Progress Tracking**: Monitor your completion rate per module, per semester, and overall degree progress.
- **To-Do List**: Built-in task manager with a daily learning streak tracker.
- **Notes**: Take and store quick notes inside the dashboard.
- **Grade Development**: Track your exam grades and see your GPA (Grade Point Average) develop over time.
- **Key Metrics**: View important statistics like your GPA and overall progress at a glance.

## Project Structure

The project is structured into modular components:

- `app.py`: The main entry point and master GUI frame for the application.
- `DataHandler_Studium.py`: Core logic for managing semesters, modules, and grade calculations (using Singleton patterns).
- `file_manager.py`: Utilities for handling JSON data persistence.
- `widgets/`: Contains all modular UI components (`ToDo_Logic`, `Notes_Logic`, `Key_Metrics_Logic`, `Modules_Semester_Logic`, `Grade_Development_Logic`).
- `visuals/`: Configuration files for styling (e.g., `settings.py`).
- `storage/`: Local JSON storage for modules, grades, and tasks.


## Installation & Usage

1. Clone this repository.
2. Ensure you have the required dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

## Language
The user interface and internal documentation are primarily in German, tailored for German-speaking students ("Mein Dashboard fürs Studium").