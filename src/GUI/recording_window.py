import os
import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import time
from datetime import datetime
from mediapipe_modules import get_pipeline_class
from recorders.recorder import Recorder
from utils.timestamp import get_timestamp

class RecordingWindow:
    def __init__(self, config):
        self.config = config

        pipeline_class = get_pipeline_class(config["pipeline"])
        if pipeline_class is None:
            raise ValueError(f"Unknown pipeline: {config['pipeline']}")
        self.pipeline = pipeline_class()

        self.window = tk.Toplevel()
        self.window.title(f"Recording - {config['name']}")

        tk.Label(self.window, text=f"Dataset: {config['name']}").pack()

        video_frame = tk.Frame(self.window)
        video_frame.pack()

        self.canvas_video = tk.Canvas(video_frame, width=640, height=480, bg="black")
        self.canvas_video.grid(row=0, column=0)

        self.canvas_landmarks = tk.Canvas(video_frame, width=640, height=480, bg="white")
        self.canvas_landmarks.grid(row=0, column=1)

        tk.Label(self.window, text="Select initial label:").pack()
        self.label_dropdown = ttk.Combobox(self.window, values=self.config["labels"])
        self.label_dropdown.pack(pady=5)
        self.label_dropdown.current(0)

        self.label_var = tk.StringVar(value="Label: none")
        tk.Label(self.window, textvariable=self.label_var).pack()

        self.progress = ttk.Progressbar(self.window, length=300, mode='determinate')
        self.progress.pack(pady=5)

        controls = tk.Frame(self.window)
        controls.pack()

        self.start_button = tk.Button(controls, text="Start Recording", command=self.start_recording)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = tk.Button(controls, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.window.bind("<Key>", self.key_pressed)

        self.running = True
        self.recording = False
        self.start_time = None
        self.recorder = None
        self.current_label = None
        self.video_writer = None
        self.video_filename = None

        self.cap = cv2.VideoCapture(0)
        self.update_frame()

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.running = False
        if self.cap:
            self.cap.release()
        if self.video_writer:
            self.video_writer.release()
        self.window.destroy()

    def start_recording(self):
        self.recording = True
        self.start_time = time.time()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.current_label = self.label_dropdown.get()

        # Create dataset-specific folder
        dataset_folder = os.path.join("data", self.config["name"])
        os.makedirs(dataset_folder, exist_ok=True)

        # Create CSV recorder
        self.recorder = Recorder(
            output_folder=dataset_folder,
            label=self.current_label,
            selected_landmarks=self.config["selected_landmarks"]
        )

        # Prepare video filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.video_filename = os.path.join(dataset_folder, f"record_{timestamp}.mp4")

    def stop_recording(self):
        self.recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        if self.recorder:
            self.recorder.close()
            self.recorder = None
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None

    def key_pressed(self, event):
        key = event.char.upper()
        if key in self.config["labels"]:
            self.current_label = key
            self.label_var.set(f"Label: {self.current_label}")
            if self.recorder:
                self.recorder.label = self.current_label

    def update_frame(self):
        if not self.running:
            return

        ret, frame = self.cap.read()
        if ret:
            if not hasattr(self, "frame_width"):
                self.frame_height, self.frame_width, _ = frame.shape

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_landmarks, landmarks_only_img, landmarks_data = self.pipeline.process(frame_rgb)

            self._draw_on_canvas(frame_landmarks, self.canvas_video)
            self._draw_on_canvas(landmarks_only_img, self.canvas_landmarks)

            if self.recording:
                # Create video writer if needed
                if self.video_writer is None:
                    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                    fps = 30
                    self.video_writer = cv2.VideoWriter(
                        self.video_filename,
                        fourcc,
                        fps,
                        (self.frame_width, self.frame_height)
                    )

                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                self.video_writer.write(frame_bgr)

            if self.recording and landmarks_data:
                for landmarks in landmarks_data:
                    selected = []
                    for idx in self.config["selected_landmarks"]:
                        base = idx * 3
                        selected.extend(landmarks[base:base+3])
                    timestamp = get_timestamp()
                    self.recorder.write(timestamp, selected)

            if self.recording:
                elapsed = time.time() - self.start_time
                time_window = self.config["time_window"]
                percent = min(100, (elapsed / time_window) * 100)
                self.progress["value"] = percent

                if elapsed >= time_window:
                    self.stop_recording()
            else:
                self.progress["value"] = 0

        self.window.after(10, self.update_frame)

    def _draw_on_canvas(self, image_bgr, canvas):
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_pil = image_pil.resize((640, 480))
        photo = ImageTk.PhotoImage(image=image_pil)
        canvas.image = photo
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
