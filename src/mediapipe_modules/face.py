import mediapipe as mp
import cv2
import numpy as np

class FacePipeline:
    def __init__(self):
        self.mp_face = mp.solutions.face_mesh
        self.face = self.mp_face.FaceMesh()
        self.drawing_utils = mp.solutions.drawing_utils

    def process(self, frame):
        results = self.face.process(frame)
        frame_with_landmarks = frame.copy()
        landmarks_only = np.ones_like(frame) * 255
        landmarks_data = []

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                self.drawing_utils.draw_landmarks(
                    frame_with_landmarks,
                    face_landmarks,
                    self.mp_face.FACEMESH_TESSELATION,
                )

                # Draw simplified landmarks on landmarks-only image
                for landmark in face_landmarks.landmark:
                    h, w, _ = frame.shape
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(landmarks_only, (x, y), 1, (0, 0, 255), -1)

                landmarks = []
                for lm in face_landmarks.landmark:
                    landmarks.extend([lm.x, lm.y, lm.z])
                landmarks_data.append(landmarks)

        return frame_with_landmarks, landmarks_only, landmarks_data
