# Sterile Interface for Surgical Environments

A **touch-free gesture control system** that allows surgeons to interact with medical images without touching any device.  
The system uses **computer vision and depth estimation** to recognize hand gestures and convert them into commands such as **next image, previous image, zoom in, and zoom out**.

This helps maintain a **sterile operating room environment**.

---

# Features

- Touch-free gesture control
- Navigate medical images
- Zoom in and zoom out
- Real-time hand tracking
- Depth-aware gesture recognition
- Webcam based system

---

# Technologies Used

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- PyTorch
- MiDaS Depth Estimation
- Webcam

---

# Project Structure

```
sterile-interface
│
├── models
│   └── model-small.onnx
│
├── images
│   ├── scan1.jpg
│   ├── scan2.jpg
│   ├── scan3.jpg
│
├── viewer.py
├── gesture_control.py
└── README.md
```

---

# System Requirements

### Operating System
```
Ubuntu 22.04 or later
```

### Hardware
```
Webcam
```

### Software
```
Python 3.10+
pip
```

---

# 1. Install Python

Check if Python is installed:

```bash
python3 --version
```

If Python is not installed:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

# 2. Install Python Virtual Environment

Ubuntu requires installing the `venv` package.

```bash
sudo apt install python3-venv
```

If using Python 3.13:

```bash
sudo apt install python3.13-venv
```

---

# 3. Create Project Folder

```bash
mkdir sterile-interface
cd sterile-interface
```

---

# 4. Create Virtual Environment

```bash
python3 -m venv venv
```

---

# 5. Activate Virtual Environment

```bash
source venv/bin/activate
```

Your terminal should look like:

```
(venv) user@system:~/sterile-interface$
```

---

# 6. Install Required Libraries

```bash
pip install opencv-python mediapipe numpy pyautogui torch torchvision
```

---

# 7. Download MiDaS Depth Model

Create models folder:

```bash
mkdir models
```

Download the model:

```bash
wget https://github.com/isl-org/MiDaS/releases/download/v2_1/model-small.onnx -P models
```

---

# 8. Add Medical Images

Create an images folder:

```bash
mkdir images
```

Add sample scan images such as:

```
scan1.jpg
scan2.jpg
scan3.jpg
```

---

# 9. Running the System

Open **two terminals**.

---

## Terminal 1 – Run Image Viewer

```bash
python viewer.py
```

This opens the **medical image viewer**.

---

## Terminal 2 – Run Gesture Detection

```bash
python gesture_control.py
```

This starts the **gesture recognition system**.

---

# Gesture Controls

| Gesture | Action |
|------|------|
Move hand right | Next image |
Move hand left | Previous image |
Move hand closer | Zoom In |
Move hand farther | Zoom Out |

---

# Example Usage

During surgery:

1. Surgeon raises hand in front of the camera  
2. Moves hand right → next MRI slice  
3. Moves hand left → previous slice  
4. Moves hand closer → zoom into scan  
5. Moves hand away → zoom out  

No physical interaction is required.

---

# Why This Project Is Useful

This project demonstrates:

- Computer Vision
- AI-based depth estimation
- Gesture recognition
- Human–computer interaction
- Healthcare technology applications

It solves a **real problem in operating rooms where surgeons cannot touch devices during surgery**.

---

# Future Improvements

Possible upgrades include:

- YOLOv11 hand detection
- 3D organ viewer
- Real CT/MRI DICOM viewer
- Gesture smoothing
- Multi-hand gestures
- GUI interface
- GPU acceleration

---

# Author

Developed as a **Computer Vision project for gesture-based sterile interfaces in surgical environments**.