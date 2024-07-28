import cv2
import mediapipe as mp
import math

# Initialisiere Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils  # Hand skeleton
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)

def run_gesture_detection(direction_callback):
    cap = cv2.VideoCapture(0)  # Öffne die Kamera
    _, frame = cap.read()  # Lese ein Frame von der Kamera
    height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right = define_rois(frame)

    while True:
        ret, frame = cap.read()  # Lese ein Frame von der Kamera
        if not ret:
            print("Fehler beim Abrufen des Bildes von der Kamera")
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)  # Horizontal spiegeln
        results = hands.process(frame_rgb)
        draw_rois(frame, height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right)

        direction = "stop"  # Standardmäßig auf "stop" setzen

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for landmark in hand_landmarks.landmark:
                    landmark.x = 1.0 - landmark.x
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                finger_y = int(index_finger_tip.y * height)
                if finger_y < roi_top:
                    direction = "up"
                elif finger_y > roi_bottom:
                    direction = "down"
                else:
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    treshold_backward = 0.1
                    treshold_forward = 0.20
                    distance = math.sqrt(
                        (index_finger_tip.x - thumb_tip.x) ** 2
                        + (index_finger_tip.y - thumb_tip.y) ** 2
                    )
                    if distance < treshold_backward:
                        direction = "backward"
                    elif distance > treshold_forward:
                        direction = "forward"
                    else:
                        if index_finger_tip.x < thumb_tip.x:
                            direction = "left"
                        elif index_finger_tip.x > thumb_tip.x:
                            direction = "right"
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        direction_callback(direction)  # Rufe die Callback-Funktion mit der erkannten Richtung auf
        cv2.imshow("Frame", frame)  # Zeige das Frame mit OpenCV an
        key = cv2.waitKey(1)  # Warte auf eine Tastatureingabe (1 ms Timeout)
        if key & 0xFF == ord("q"):  # Beende die Schleife, wenn 'q' gedrückt wird
            break

    cap.releas1e()  # Gib die Ressourcen frei
    cv2.destroyAllWindows()

def draw_rois(frame, height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right):
    cv2.rectangle(frame, (roi_middle_left, roi_top), (roi_middle_right, roi_bottom), (0, 255, 0), 2)
    cv2.rectangle(frame, (0, 0), (width, roi_top), (255, 0, 0), 2)
    cv2.rectangle(frame, (0, roi_bottom), (width, height), (255, 0, 0), 2)

def define_rois(frame):
    height, width, _ = frame.shape
    roi_top = int(height / 4)
    roi_bottom = int(3 * height / 4)
    roi_middle_left = int(width / 4)
    roi_middle_right = int(3 * width / 4)
    return height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right

if __name__ == "__main__":
    run_gesture_detection(lambda direction: print(f"gesturedetection.py {direction}"))
