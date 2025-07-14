import mediapipe as mp
import cv2
import numpy as np

class PosePipeline:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.drawing_utils = mp.solutions.drawing_utils

    def process(self, frame):
        results = self.pose.process(frame)
        frame_with_landmarks = frame.copy()
        landmarks_only = np.ones_like(frame) * 255
        landmarks_data = []

        if results.pose_landmarks:
            self.drawing_utils.draw_landmarks(
                frame_with_landmarks,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
            )
            for connection in self.mp_pose.POSE_CONNECTIONS:
                start_idx, end_idx = connection
                start = results.pose_landmarks.landmark[start_idx]
                end = results.pose_landmarks.landmark[end_idx]

                h, w, _ = frame.shape
                x1, y1 = int(start.x * w), int(start.y * h)
                x2, y2 = int(end.x * w), int(end.y * h)
                cv2.line(landmarks_only, (x1, y1), (x2, y2), (0, 0, 255), 2)

            landmarks = []
            for lm in results.pose_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])
            landmarks_data.append(landmarks)

        return frame_with_landmarks, landmarks_only, landmarks_data
