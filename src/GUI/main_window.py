import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import json
from tkinter import ttk

from GUI import landmark_selector

DATASET_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'datasets')
os.makedirs(DATASET_FOLDER, exist_ok=True)

class MainWindow:
    def __init__(self, master, launch_recording_callback):
        self.master = master
        self.master.title("Mediapipe Data Collector")

        self.dataset_listbox = tk.Listbox(master, width=50, height=10)
        self.dataset_listbox.pack(pady=10)

        button_frame = tk.Frame(master)
        button_frame.pack()

        self.refresh_button = tk.Button(button_frame, text="Refresh List", command=self.load_datasets)
        self.refresh_button.grid(row=0, column=0, padx=5, pady=5)

        self.create_button = tk.Button(button_frame, text="Create New Dataset", command=self.create_dataset_dialog)
        self.create_button.grid(row=0, column=1, padx=5, pady=5)

        self.edit_button = tk.Button(button_frame, text="Edit Dataset", command=self.edit_dataset)
        self.edit_button.grid(row=0, column=2, padx=5, pady=5)

        self.delete_button = tk.Button(button_frame, text="Delete Dataset", command=self.delete_dataset)
        self.delete_button.grid(row=0, column=3, padx=5, pady=5)

        self.open_button = tk.Button(master, text="Open Selected Dataset", command=self.open_dataset)
        self.open_button.pack(pady=10)

        self.launch_recording_callback = launch_recording_callback

        self.load_datasets()

    def load_datasets(self):
        self.dataset_listbox.delete(0, tk.END)

        for filename in os.listdir(DATASET_FOLDER):
            if filename.endswith(".json"):
                path = os.path.join(DATASET_FOLDER, filename)
                try:
                    with open(path) as f:
                        data = json.load(f)
                        name = data.get("name", filename)
                        self.dataset_listbox.insert(tk.END, f"{name} ({filename})")
                except json.JSONDecodeError:
                    self.dataset_listbox.insert(tk.END, f"[Invalid JSON] {filename}")

    def create_dataset_dialog(self, prefill=None, filename=None):
        window = tk.Toplevel(self.master)
        window.title("Create/Edit Dataset")
        landmark_selector_frame = None
        landmark_selector_widget = None

        def on_pipeline_change(event=None):
            nonlocal landmark_selector_widget
            # Clear old widget
            for child in landmark_selector_frame.winfo_children():
                child.destroy()

            selected_pipeline = pipeline_var.get()
            # Create new landmark selector
            landmark_selector_widget = landmark_selector.LandmarkSelector(
                landmark_selector_frame,
                pipeline=selected_pipeline,
                selected_landmarks=set()
            )
            landmark_selector_widget.pack()
        # Name
        tk.Label(window, text="Dataset Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        name_var = tk.StringVar(value=prefill["name"] if prefill else "")
        tk.Entry(window, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

        # Pipeline dropdown
        tk.Label(window, text="Pipeline:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        pipeline_var = tk.StringVar(value=prefill["pipeline"] if prefill else "hands")
        pipeline_menu = ttk.Combobox(window, textvariable=pipeline_var, values=["hands", "pose", "face"])
        pipeline_menu.grid(row=1, column=1, padx=5, pady=5)
        pipeline_menu.bind("<<ComboboxSelected>>", on_pipeline_change)

        # Frame to hold the landmark selector UI
        landmark_selector_frame = tk.Frame(window)
        landmark_selector_frame.grid(row=4, column=0, columnspan=2, pady=10)
        # Time window
        tk.Label(window, text="Time Window (s):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        time_window_var = tk.StringVar(value=str(prefill["time_window"]) if prefill else "")
        tk.Entry(window, textvariable=time_window_var).grid(row=2, column=1, padx=5, pady=5)

        # Labels
        tk.Label(window, text="Labels (comma-separated):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        labels_var = tk.StringVar(value=",".join(prefill["labels"]) if prefill else "")
        tk.Entry(window, textvariable=labels_var).grid(row=3, column=1, padx=5, pady=5)
        if prefill:
            on_pipeline_change()
        def save_dataset():
            name = name_var.get().strip()
            pipeline = pipeline_var.get().strip()
            time_window_str = time_window_var.get().strip()
            labels_str = labels_var.get().strip()

            if not name or not pipeline or not time_window_str or not labels_str:
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                time_window = float(time_window_str)
            except ValueError:
                messagebox.showerror("Error", "Time window must be a number.")
                return

            labels = [label.strip() for label in labels_str.split(",") if label.strip()]
            selected_landmarks = landmark_selector_widget.get_selected_landmarks()

            dataset_config = {
                "name": name,
                "pipeline": pipeline,
                "time_window": time_window,
                "labels": labels,
                "selected_landmarks": selected_landmarks
            }

            if filename is None:
                filename_final = f"{name}.json"
            else:
                filename_final = filename

            path = os.path.join(DATASET_FOLDER, filename_final)
            with open(path, "w") as f:
                json.dump(dataset_config, f, indent=4)

            messagebox.showinfo("Saved", f"Dataset '{name}' saved successfully.")
            self.load_datasets()
            window.destroy()
        
        
        tk.Button(window, text="Save", command=save_dataset).grid(row=4, column=0, columnspan=2, pady=10)

    def delete_dataset(self):
        selection = self.dataset_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a dataset to delete.")
            return

        item_text = self.dataset_listbox.get(selection[0])
        filename = item_text.split("(")[-1].rstrip(")")
        path = os.path.join(DATASET_FOLDER, filename)

        if messagebox.askyesno("Confirm Delete", f"Delete dataset '{filename}'?"):
            os.remove(path)
            self.load_datasets()

    def edit_dataset(self):
        selection = self.dataset_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a dataset to edit.")
            return

        item_text = self.dataset_listbox.get(selection[0])
        filename = item_text.split("(")[-1].rstrip(")")
        path = os.path.join(DATASET_FOLDER, filename)

        with open(path) as f:
            config = json.load(f)

        self.create_dataset_dialog(prefill=config, filename=filename)

    def open_dataset(self):
        selection = self.dataset_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a dataset to open.")
            return

        item_text = self.dataset_listbox.get(selection[0])
        filename = item_text.split("(")[-1].rstrip(")")
        path = os.path.join(DATASET_FOLDER, filename)

        with open(path) as f:
            config = json.load(f)

        # Pass config to recording window
        self.launch_recording_callback(config)
    
    

