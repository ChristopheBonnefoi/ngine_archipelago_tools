import tkinter as tk
from tkinter import ttk

from gui.log_splitter_gui import LogSplitterGUI
from gui.hatsune_miku_gui import HatsuneMikuGUI
from gui.hint_manager_gui import HintManagerGUI

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NGine Archipelago Tools")
        self.geometry("900x600")

        # Créer le notebook
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # Initialiser les onglets
        log_splitter_tab = LogSplitterGUI(notebook)
        hatsune_miku_tab = HatsuneMikuGUI(notebook)
        hint_manager_tab = HintManagerGUI(notebook)

        # Ajouter les onglets
        notebook.add(log_splitter_tab, text="Log Splitter")
        notebook.add(hatsune_miku_tab, text="Hatsune Miku Tracker")
        notebook.add(hint_manager_tab, text="Hint Manager")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()