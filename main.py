import cv2 as cv
import mouse
import numpy as np
import time
import mediapipe as mp
import tensorflow as tf



def guesture():
    swidth, sheight = 700, 600

    x1, x2 = 85, 550
    y1, y2 = 85, 400

    vid = cv.VideoCapture(0)
    vid.set(3, swidth)
    vid.set(4, sheight)
    ptime = 0


    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.2)
    draw = mp.solutions.drawing_utils


    while True:
        rec, frame = vid.read()
        h, w, c = frame.shape
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime

        frame=cv.flip(frame, 1)
        cv.rectangle(frame, (x1, y1), (x2, y2), (250, 0, 0), 3)

        cv.putText(frame, f'FPS:{int(fps)}', (23, 60), cv.QT_FONT_NORMAL, 1, (190, 37, 155), 2)
        ##convert to BGR 2 RGB
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False
        result = hands.process(frame_rgb)


        ##convet back to RGB 2 BGR
        frame_rgb = cv.cvtColor(frame_rgb, cv.COLOR_RGB2BGR)
       # print("handed:", result.multi_handedness)

        ##single hand detection

        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for ids, lm in enumerate(handslms.landmark):
                    lmx = int(lm.x * w) ##x co ordinate of hand
                    lmy = int(lm.y * h) ##y co ordinate of hand
                    landmarks.append([ids, lmx, lmy])

                    if ids==8:
                        cv.circle(frame_rgb, (lmx, lmy), 15, (0, 0, 255), cv.FILLED)
                        mouse.move(lmx, lmy, absolute=True, duration= 0)
                draw.draw_landmarks(frame_rgb, handslms, mpHands.HAND_CONNECTIONS,
                                    draw.DrawingSpec(color=(190, 37, 155), thickness=4, circle_radius=5),

                                    draw.DrawingSpec(color=(0, 128, 255), thickness=4, circle_radius=5))


            # print(landmarks)
            # for hand_landmarks in result.multi_hand_landmarks:
            #
            #     x = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].x * 1920
            #     y = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].y * 1080
            #     #qcv.circle(frame_rgb, (x, y), 13, (255, 0, 255), cv.FILLED)
            #     mouse.move(x, y, absolute=True, duration=0)
        ##display the capture vid
        frame_rgb.flags.writeable = True
        cv.imshow("frame", frame_rgb)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break
    vid.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    guesture()
