import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import pyautogui
import onnxruntime as ort
import urllib.request
import os
import time

# Download hand landmarker model if not exists
MODEL_PATH = "hand_landmarker.task"
if not os.path.exists(MODEL_PATH):
    print("Downloading hand landmarker model...")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
        MODEL_PATH
    )

# Initialize webcam - try multiple backends/indices
def init_camera():
    """Try different camera indices and backends"""
    for idx in [0, 1, 2]:
        # Try V4L2 backend first (Linux)
        cap = cv2.VideoCapture(idx, cv2.CAP_V4L2)
        if cap.isOpened():
            print(f"Camera opened with V4L2 backend at index {idx}")
            return cap
        cap.release()
        
        # Try default backend
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            print(f"Camera opened at index {idx}")
            return cap
        cap.release()
    
    return None

cap = init_camera()
if cap is None:
    print("ERROR: Could not open any camera!")
    print("Make sure your webcam is connected and not in use by another app.")
    print("Try: ls /dev/video*")
    exit(1)

# Setup hand landmarker with new API
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2
)
detector = vision.HandLandmarker.create_from_options(options)

prev_x = None
prev_depth = None

# Cooldown settings to prevent glitchy repeated inputs
COOLDOWN_TIME = 0.5  # seconds between gesture triggers
last_gesture_time = 0
last_zoom_time = 0

# Thresholds
SWIPE_THRESHOLD = 60  # pixels for left/right swipe
DEPTH_THRESHOLD = 0.5  # depth change for zoom

# Load MiDaS ONNX model
midas_session = ort.InferenceSession("models/model-small.onnx")
midas_input_name = midas_session.get_inputs()[0].name

def preprocess_for_midas(img):
    """Preprocess image for MiDaS small model"""
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (256, 256))
    img = img.astype(np.float32) / 255.0
    img = (img - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    img = img.transpose(2, 0, 1)
    img = np.expand_dims(img, axis=0).astype(np.float32)
    return img

print("Gesture Control Started!")
print("- Swipe left/right to change images")
print("- Move hand forward/backward to zoom")
print("- Press 'q' or ESC to quit")
print("-" * 40)

while True:

    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    frame = cv2.flip(frame,1)
    current_time = time.time()

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert to mediapipe Image format
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    results = detector.detect(mp_image)

    if results.hand_landmarks:

        for hand in results.hand_landmarks:

            x = int(hand[8].x * frame.shape[1])
            y = int(hand[8].y * frame.shape[0])

            cv2.circle(frame,(x,y),10,(0,255,0),-1)

            # ---------- LEFT RIGHT DETECTION ----------

            if prev_x is not None and (current_time - last_gesture_time) > COOLDOWN_TIME:

                diff = x - prev_x

                if diff > SWIPE_THRESHOLD:
                    pyautogui.press("right")
                    print("NEXT IMAGE")
                    last_gesture_time = current_time
                    prev_x = None  # Reset to prevent chained triggers

                elif diff < -SWIPE_THRESHOLD:
                    pyautogui.press("left")
                    print("PREVIOUS IMAGE")
                    last_gesture_time = current_time
                    prev_x = None  # Reset to prevent chained triggers

            if prev_x is not None:
                prev_x = x  # Smooth update
            else:
                prev_x = x
    else:
        # Reset when hand not detected
        prev_x = None

    # -------- DEPTH ESTIMATION (with cooldown) --------

    if (current_time - last_zoom_time) > COOLDOWN_TIME:
        input_batch = preprocess_for_midas(frame)
        prediction = midas_session.run(None, {midas_input_name: input_batch})[0]

        depth = prediction.mean()

        if prev_depth is not None:

            depth_diff = depth - prev_depth

            if depth_diff > DEPTH_THRESHOLD:
                pyautogui.press('+')
                print("ZOOM IN")
                last_zoom_time = current_time

            elif depth_diff < -DEPTH_THRESHOLD:
                pyautogui.press('-')
                print("ZOOM OUT")
                last_zoom_time = current_time

        prev_depth = depth

    cv2.imshow("Gesture Camera", frame)

    # Check for quit: ESC (27) or 'q' (113)
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)  # Extra call to ensure window closes