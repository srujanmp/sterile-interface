import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import torch

# Initialize webcam
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

prev_x = None
prev_depth = None

# Load MiDaS
midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")
midas.eval()

transform = torch.hub.load("intel-isl/MiDaS", "transforms").small_transform

while True:

    ret, frame = cap.read()

    frame = cv2.flip(frame,1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand in results.multi_hand_landmarks:

            x = int(hand.landmark[8].x * frame.shape[1])
            y = int(hand.landmark[8].y * frame.shape[0])

            cv2.circle(frame,(x,y),10,(0,255,0),-1)

            # ---------- LEFT RIGHT DETECTION ----------

            if prev_x is not None:

                diff = x - prev_x

                if diff > 40:
                    pyautogui.press("right")
                    print("NEXT IMAGE")

                elif diff < -40:
                    pyautogui.press("left")
                    print("PREVIOUS IMAGE")

            prev_x = x

    # -------- DEPTH ESTIMATION --------

    input_batch = transform(frame).unsqueeze(0)

    with torch.no_grad():
        prediction = midas(input_batch)

    depth = prediction.mean().item()

    if prev_depth is not None:

        if depth - prev_depth > 0.02:
            pyautogui.press('+')
            print("ZOOM IN")

        elif depth - prev_depth < -0.02:
            pyautogui.press('-')
            print("ZOOM OUT")

    prev_depth = depth

    cv2.imshow("Gesture Camera", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()