import tkinter as tk

from mediapipe_modules import landmark_positions, landmark_connections

class LandmarkSelector(tk.Frame):
    def __init__(self, parent, pipeline, selected_landmarks=None):
        super().__init__(parent)
        self.pipeline = pipeline
        self.selected_landmarks = selected_landmarks or set()

        # Canvas size
        self.canvas_size = 500
        self.canvas = tk.Canvas(self, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack()

        # Load data
        self.landmarks = landmark_positions[pipeline]
        self.connections = landmark_connections.get(pipeline, [])

        self.canvas.bind("<Button-1>", self.on_click)
        self._draw_skeleton()

    def _draw_skeleton(self):
        self.canvas.delete("all")

        # Draw connections
        for a, b in self.connections:
            xa, ya = self.landmarks[a]
            xb, yb = self.landmarks[b]
            self.canvas.create_line(xa, ya, xb, yb, fill="gray", width=2)

        # Draw landmarks
        for idx, (x, y) in enumerate(self.landmarks):
            color = "green" if idx in self.selected_landmarks else "blue"
            self.canvas.create_oval(
                x - 5, y - 5, x + 5, y + 5,
                fill=color, outline=""
            )
            self.canvas.create_text(
                x, y - 10,
                text=str(idx),
                fill="black",
                font=("Arial", 8)
            )

    def on_click(self, event):
        for idx, (x, y) in enumerate(self.landmarks):
            if abs(event.x - x) < 10 and abs(event.y - y) < 10:
                if idx in self.selected_landmarks:
                    self.selected_landmarks.remove(idx)
                else:
                    self.selected_landmarks.add(idx)
                self._draw_skeleton()
                break

    def get_selected_landmarks(self):
        return list(sorted(self.selected_landmarks))