import csv
import os
from datetime import datetime

class Recorder:
    def __init__(self, output_folder, label, selected_landmarks):
        os.makedirs(output_folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = os.path.join(output_folder, f"record_{timestamp}.csv")
        self.label = label
        self.file = open(self.filename, "w", newline="")
        self.writer = csv.writer(self.file)

        # Write header
        header = ["timestamp"]
        for idx in selected_landmarks:
            header += [f"l{idx}_x", f"l{idx}_y", f"l{idx}_z"]
        header.append("label")
        self.writer.writerow(header)

    def write(self, timestamp, landmarks):
        row = [timestamp] + landmarks + [self.label]
        self.writer.writerow(row)

    def close(self):
        self.file.close()
