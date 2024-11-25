import cv2
import mediapipe as mp
import pyautogui
#ARUN.S hand gesture project
x1 = y1 = x2 = y2 = 0
webcam = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

while True:
    ret, image = webcam.read()
    image = cv2.flip(image, 1)
    frame_height, frame_width, _ = image.shape  # Typo corrected (frame_width instead of frame_weidh)

    # Correct capitalization of cvtColor
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                # Index finger tip (id=8) and thumb tip (id=4)
                if id == 8:
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                    x1 = x
                    y1 = y
                if id == 4:
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 0, 255), thickness=3)
                    x2 = x
                    y2 = y

        # Calculate distance and adjust volume
        dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5  # Distance calculation fixed
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)

        if dist > 50:
            pyautogui.press("volumeup")
        else:
            pyautogui.press("volumedown")

    cv2.imshow("Hand volume control by arun", image)

    # Exit on 'ESC' key press
    key = cv2.waitKey(10)  # Corrected capitalization (waitKey instead of waitkey)
    if key == 27:  # ESC key
        break

webcam.release()