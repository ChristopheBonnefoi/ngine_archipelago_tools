import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import time
import threading
import winsound

from modules.log_splitter import parse_spoiler_log, write_logs_by_sender

class LogSplitterGUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.file_path_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.overwrite_all = False
        self.skip_all = False

        tk.Label(self, text="Sélectionnez le fichier log ou texte :").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.file_path_var, width=50).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(self, text="Parcourir...", command=self.select_file).grid(row=0, column=2, padx=10, pady=5)

        tk.Label(self, text="Sélectionnez le dossier de destination :").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.output_dir_var, width=50).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self, text="Parcourir...", command=self.select_output_dir).grid(row=1, column=2, padx=10, pady=5)

        tk.Button(self, text="Lancer le traitement", command=self.start_processing).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self, text="Réinitialiser", command=self.reset_interface).grid(row=2, column=2, pady=10)

        self.progress = ttk.Progressbar(self, orient="horizontal", length=600, mode="determinate")
        self.progress.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        self.eta_label = tk.Label(self, text="ETA : --:--")
        self.eta_label.grid(row=4, column=0, columnspan=3)

        self.log_box = tk.Text(self, height=15, width=100, state='disabled')
        self.log_box.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    def log(self, message):
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, f"{message}\n")
        self.log_box.see(tk.END)
        self.log_box.config(state='disabled')

    def reset_interface(self):
        self.progress["value"] = 0
        self.eta_label.config(text="ETA : --:--")
        self.log_box.config(state='normal')
        self.log_box.delete(1.0, tk.END)
        self.log_box.config(state='disabled')
        self.overwrite_all = False
        self.skip_all = False

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Sélectionnez le fichier spoiler.log ou .txt",
            filetypes=[("Log and Text Files", "*.log *.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)

    def select_output_dir(self):
        output_dir = filedialog.askdirectory(title="Sélectionnez le dossier de destination")
        if output_dir:
            self.output_dir_var.set(output_dir)

    def start_processing(self):
        thread = threading.Thread(target=self.process_log)
        thread.start()

    def build_bar(self, width=20):
        return "[" + "#" * width + "]"

    def ask_overwrite_checkbox(self, filename):
        window = tk.Toplevel(self)
        window.title("Fichier existant")
        window.geometry("400x150")
        window.resizable(False, False)

        label = tk.Label(window, text=f"Le fichier '{filename}' existe déjà.\nVoulez-vous l'écraser ?", justify="left", anchor="w")
        label.pack(pady=10, padx=10, anchor="w")

        check_var = tk.IntVar()
        check = tk.Checkbutton(window, text="Ne plus demander pour les suivants", variable=check_var)
        check.pack(pady=5, padx=10, anchor="w")

        response = {"value": None}

        def validate(choice):
            response["value"] = (choice, check_var.get() == 1)
            window.destroy()

        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Oui", width=10, command=lambda: validate("yes")).pack(side=tk.TOP, pady=2)
        tk.Button(btn_frame, text="Non", width=10, command=lambda: validate("no")).pack(side=tk.TOP)

        window.grab_set()
        self.wait_window(window)
        return response["value"]

    def process_log(self):
        file_path = self.file_path_var.get()
        output_dir = self.output_dir_var.get()

        if not file_path or not os.path.isfile(file_path):
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier log ou texte valide.")
            return

        if not output_dir:
            messagebox.showerror("Erreur", "Veuillez sélectionner un dossier de destination.")
            return

        self.reset_interface()
        start_time = time.time()

        bar = self.build_bar()
        self.log(f"📄 Lecture du fichier {bar} 100%")

        player_settings, sender_data, receiver_data, player_info = parse_spoiler_log(file_path)
        total_players = len(player_info)
        if total_players == 0:
            self.log("❌ Aucun joueur détecté.")
            return

        self.progress["maximum"] = total_players
        bar = self.build_bar()
        self.log(f"✅ {total_players} joueurs détectés. Début du traitement {bar} 100%")

        for i, (player_name, formatted_name) in enumerate(player_info.items(), 1):
            elapsed = time.time() - start_time
            remaining = (elapsed / i) * (total_players - i)
            eta_min = int(remaining // 60)
            eta_sec = int(remaining % 60)
            self.eta_label.config(text=f"ETA : {eta_min:02d}:{eta_sec:02d}")

            bar = self.build_bar()
            file_name = f"{formatted_name}_spoiler.log"
            full_path = os.path.join(output_dir, file_name)

            if os.path.exists(full_path) and not (self.overwrite_all or self.skip_all):
                choice, remember = self.ask_overwrite_checkbox(file_name)
                if choice == "no":
                    self.log(f"⏩ {file_name} ignoré (existe déjà)")
                    if remember:
                        self.skip_all = True
                        self.log("📝 Mode 'Tout ignorer' activé pour les fichiers suivants.")
                    continue
                elif choice == "yes":
                    if remember:
                        self.overwrite_all = True
                        self.log("📝 Mode 'Tout écraser' activé pour les fichiers suivants.")
                elif choice == "yes":
                    if remember:
                        self.overwrite_all = True

            if self.skip_all:
                self.log(f"⏩ {file_name} ignoré (mode 'ne pas écraser')")
                continue

            self.log(f"🛠 Traitement de {formatted_name} {bar} 100% - ({i}/{total_players})")

            single_sender = {player_name: sender_data.get(player_name, {})}
            single_receiver = {player_name: receiver_data.get(player_name, {})}
            single_settings = {player_name: player_settings.get(player_name, "")}
            write_logs_by_sender(single_settings, single_sender, single_receiver, {player_name: formatted_name}, output_dir)

            self.progress["value"] = i
            self.progress.update()

        self.eta_label.config(text="ETA : 00:00")
        self.log("✔️ Tous les fichiers ont été générés avec succès.")
        winsound.MessageBeep()
        winsound.MessageBeep()
