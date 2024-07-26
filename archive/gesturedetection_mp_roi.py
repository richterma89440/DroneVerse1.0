import cv2
import mediapipe as mp


def draw_hand_skeleton(image_flipped, results, mp_hands):

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(
                image_flipped, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )


def start_roibased_gesture_detection(image_flipped, direction, hands, mp_hands):

    # Define top and bottom Rois
    height, width, _ = image_flipped.shape
    roi_top = int(height / 4)
    roi_bottom = int(3 * height / 4)
    roi_middle_left = int(width / 4)
    roi_middle_right = int(3 * width / 4)

    # Draw Rois -> gestenerkennung elend langsam wenn aktiviert
    draw_rois(image_flipped, roi_top, roi_bottom, roi_middle_left, roi_middle_right)

    # draw_hand_skeleton(image_flipped, results, mp_hands)

    results = hands.process(image_flipped)

    # Überprüfe, ob der Zeigefinger der rechten Hand in der oberen, unteren oder mittleren Region liegt
    # Gestenerkennung nur für rechte hand
    if results.multi_handedness and results.multi_hand_landmarks:
        for hand_handedness, hand_landmarks in zip(
            results.multi_handedness, results.multi_hand_landmarks
        ):
            handedness = hand_handedness.classification[0].label
            if handedness == "Right":  # Nur rechte Hand berücksichtigen
                index_finger_tip = hand_landmarks.landmark[
                    mp_hands.HandLandmark.INDEX_FINGER_TIP
                ]
                finger_y = int(index_finger_tip.y * height)

                # Finger oben
                if finger_y < roi_top:
                    direction = "up"
                    print(direction)

                # Finger unten
                elif finger_y > roi_bottom:
                    direction = "down"
                    print(direction)

                else:
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                    # Finger rechts
                    if index_finger_tip.x < thumb_tip.x:
                        direction = "left"
                        print(direction)

                    # Finger links
                    elif index_finger_tip.x > thumb_tip.x:
                        direction = "right"
                        print(direction)

                    # Kein Finger
                    else:
                        direction = "none"
                        print(direction)


def draw_rois(image_flipped, roi_top, roi_bottom, roi_middle_left, roi_middle_right):
    height, width, _ = image_flipped.shape
    cv2.rectangle(
        image_flipped,
        (roi_middle_left, roi_top),
        (roi_middle_right, roi_bottom),
        (0, 255, 0),
        2,
    )
    cv2.rectangle(image_flipped, (0, 0), (width, roi_top), (255, 0, 0), 2)
    cv2.rectangle(image_flipped, (0, roi_bottom), (width, height), (255, 0, 0), 2)
