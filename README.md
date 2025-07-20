
# 📸 Label-It – AI Gesture Data Labeling Tool
**Part of the [FlexiScan](#) Project – A Vision-Driven Gesture Recognition Platform**

Label-It is a custom Python application for collecting and labeling gesture data using live video and MediaPipe landmarks. It helps researchers and developers create clean, organized datasets for training ML models in hand tracking, human pose estimation, sign language recognition, and more.

---

## 🚀 Features

- 🎥 **Live Camera Preview** – See real-time webcam feed with MediaPipe landmarks.
- ✋ **Landmark Detection** – Choose from Hand, Pose, Face, or Holistic landmarks.
- 🟢 **Interactive Landmark Picker** – Click to select specific landmarks; selected ones turn green.
- 🏷️ **Label Assignment** – Easily assign a label to each recording session via dropdown.
- 📁 **Dataset Management** – Organize recordings by dataset and label folders.
- 📊 **CSV Export** – Landmark coordinates saved per frame with timestamps.
- 🎞️ **Video Recording** – Synchronized `.mp4` video saved alongside data.
- 🧩 **Extensible Design** – Easily integrate new sensors or model pipelines.

---

## 📂 Folder Structure

```
Label-It/
├── src/
│   ├── GUI/
│   │   ├── recording_window.py
│   │   └── ...
│   ├── utils/
│   └── ...
├── data/
│   ├── dataset_1/
│   │   ├── label_1/
│   │   └── label_2/
│   └── dataset_2/
├── README.md
└── requirements.txt
```

---

## 🛠️ How to Run

1. **Clone the repo**:
    ```bash
    git clone https://github.com/your-username/label-it
    cd label-it
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```bash
    python src/main.py
    ```

---

## 📸 Screenshots

<!-- Add your own screenshots -->
<img src="docs/preview.png" width="600" alt="Live Recording UI"/>

---

## ⚙️ Tech Stack

- Python 3.10+
- Tkinter (GUI)
- MediaPipe (Landmark Detection)
- OpenCV (Camera & Video Handling)
- CSV, JSON, MP4 formats

---

## 📌 Use Cases

- Gesture & motion dataset collection
- AI-powered sign language labeling
- Pose-based rehabilitation dataset generation
- Hand/face/pose alignment for ML pipelines

---

## 🧠 Part of the FlexiScan Project

This tool supports **FlexiScan** — a vision-based gesture recognition project enabling contactless interaction in healthcare, accessibility, and smart environments.

---

## 👨‍💻 Author

**Mohammed Sherif**  
Computer Science Student, Suez University  
📬 mohamed.ms5517@gmail.com  
🌐 [LinkedIn](https://www.linkedin.com/in/your-profile)

---

## 📝 License

This project is licensed under the MIT License.
