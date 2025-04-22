# 🎥 Apllication to Generate Animations Using Motion Capture Technique

This project uses **MediaPipe** and **Unreal Engine 5** to generate realistic 3D character animations from recorded video. It leverages motion-capture techniques to extract pose keypoints and maps them to a 3D skeleton for animation rendering.

---

## 🧠 Overview

- 📹 Input: Pre-recorded video containing human movement
- 🤖 Pose Detection: MediaPipe extracts keypoints frame-by-frame
- 🖥️ Interface: Built with Python using the Pygame library
- 🎮 Animation: Generated and rendered using Unreal Engine 5
- 📄 Output: JSON data of keypoints + 3D animation preview

---

---

## 🚀 Tech Stack

| Area              | Technology                  |
|-------------------|-----------------------------|
| UI Development    | Python, Pygame              |
| Pose Detection    | MediaPipe (BlazePose Model) |
| Animation Engine  | Unreal Engine 5             |
| Data Format       | JSON                        |
| Visualization     | 2D overlays on video frames |

---

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/animation-motion-capture.git
   cd animation-motion-capture
2. Set up the virtual environment:
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate

3.Install dependencies:
``bash
    pip install -r requirements.txt

4.Run The Application
```bash
  MainFrame.py
