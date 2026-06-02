# ♻️ Smart Conveyor AI: Virtual Garbage Sorting System

A premium **Virtual Smart AI Conveyor Belt Dashboard** built with **YOLOv8** object tracking and **Streamlit**. This application is designed to simulate a real-world automated garbage sorting conveyor belt using a standard webcam or video feed.

---

## 🌟 Key Features

*   **Real-time YOLOv8 Tracking**: Tracks incoming garbage items (plastic, paper, glass, metal, etc.) using state-of-the-art computer vision.
*   **Virtual Sorting Line**: A vertical sorting line running down the center of the video feed. Items crossing the line trigger detection and counting events.
*   **Unique Tracking IDs**: Employs continuous tracking so each object is counted **only once** upon crossing.
*   **Virtual Servo Actuator Alert**: Visual simulation of sorting hardware. A flashing **🔴 SERVO ACTIVATED** alert is overlaid directly on the video when an item is sorted.
*   **Glassmorphic Analytics Dashboard**: Premium dark-mode UI displaying live stats, total counts, session history, and interactive distribution charts.
*   **Persistent Database**: Logged data is stored locally in a SQLite database (`garbage_stats.db`) for long-term analytics.

---

## 🛠️ Tech Stack

*   **Computer Vision**: OpenCV (`cv2`), Ultralytics (`YOLOv8`)
*   **Web Framework**: Streamlit (Premium Custom CSS customization)
*   **Data Processing**: Pandas
*   **Database**: SQLite3
*   **Language**: Python 3.x

---

## 📦 Project Structure

```text
Garbage_Sorting_AI/
│
├── app.py                 # Main Streamlit Web Application (UI, Camera Loop, & Charts)
├── database.py            # SQLite database initializer and operations
├── requirements.txt       # Python dependencies
├── best.pt                # Custom trained YOLOv8 model weights
├── train_yolo.py          # Script used to train the YOLO model
├── resume_yolo.py         # Script to resume training if interrupted
└── README.md              # Project documentation
```

---

## 🚀 Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Ruchira-Rukshan/smart-conveyor-ai.git
cd smart-conveyor-ai
```

### 2. Install Dependencies
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Place Model Weights
Make sure your custom-trained YOLO weights are saved as `best.pt` inside the project root folder.

### 4. Run the Application
Start the Streamlit dashboard:
```bash
streamlit run app.py
```

---

## 🖥️ User Interface Overview

*   **Live Camera Tab**: Turn the camera stream ON/OFF, see live detections, vertical line crossing markers, and see real-time servo triggers.
*   **Analytics Dashboard Tab**: Visualize total sorting counts, custom bar charts, and data history with filter options.

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

---

## 📄 License
This project is licensed under the MIT License.
