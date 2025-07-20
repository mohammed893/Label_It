import tkinter as tk
from GUI.main_window import MainWindow
from GUI.recording_window import RecordingWindow

def launch_recording(config):
    RecordingWindow(config)
if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap('F:/My_Projects/flexi-data/Label_It/src/assets/flexi.ico')
    app = MainWindow(root, launch_recording_callback=launch_recording)
    root.mainloop()