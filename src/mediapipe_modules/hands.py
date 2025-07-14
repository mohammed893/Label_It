import mediapipe as mp
import cv2
import numpy as np

class HandsPipeline:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

        self.drawing_utils = mp.solutions.drawing_utils
        self.connections = self.mp_hands.HAND_CONNECTIONS

    def process(self, frame):
        """
        frame: RGB image
        returns:
            frame_with_landmarks
            landmarks_only_image
            landmarks_data
        """
        results = self.hands.process(frame)
        frame_with_landmarks = frame.copy()
        landmarks_data = []

        # Create blank landmarks-only image
        landmarks_only = np.ones_like(frame) * 255  # white background

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw on original frame
                self.drawing_utils.draw_landmarks(
                    frame_with_landmarks, hand_landmarks, self.connections
                )

                # Draw on landmarks-only image
                for connection in self.connections:
                    start_idx, end_idx = connection
                    start = hand_landmarks.landmark[start_idx]
                    end = hand_landmarks.landmark[end_idx]

                    h, w, _ = frame.shape
                    x1, y1 = int(start.x * w), int(start.y * h)
                    x2, y2 = int(end.x * w), int(end.y * h)
                    cv2.line(landmarks_only, (x1, y1), (x2, y2), (0, 0, 255), 2)

                # Save landmarks as numbers
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.extend([lm.x, lm.y, lm.z])
                landmarks_data.append(landmarks)

        return frame_with_landmarks, landmarks_only, landmarks_data