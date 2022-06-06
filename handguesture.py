import cv2 as cv
import mouse
import time
import mediapipe as mp


class virtual_hand:
    def __init__(self):

        self.landmarks = None
        self.result = None
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=True,
                                        max_num_hands=1,
                                        min_detection_confidence=0.2,
                                        min_tracking_confidence=0.5)

        self.draw = mp.solutions.drawing_utils
        self.idtip = [4, 8, 12, 16, 20]

    def tracking(self, img, draw=True):
        frame_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.result = self.hands.process(frame_rgb)
        img1 = cv.cvtColor(frame_rgb, cv.COLOR_RGB2BGR)
        if draw:
            if self.result.multi_hand_landmarks:
                for hands_lms in self.result.multi_hand_landmarks:
                    self.draw.draw_landmarks(img1, hands_lms, self.mpHands.HAND_CONNECTIONS,
                                             self.draw.DrawingSpec(color=(190, 37, 155), thickness=4, circle_radius=5),
                                             self.draw.DrawingSpec(color=(0, 128, 255), thickness=4, circle_radius=5))

        return img1

    def position(self, img, hand_no=0, draw=True):

        self.landmarks = []
        if self.result.multi_hand_landmarks:
            my_hand = self.result.multi_hand_landmarks[hand_no]
            for ids, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                lmx = int(lm.x * w)  # x co_ordinate of hand
                lmy = int(lm.y * h)  # y co_ordinate of hand
                self.landmarks.append([ids, lmx, lmy])
                # if draw:
                #     if ids == 8:
                #         cv.circle(img, (lmx, lmy), 15, (255, 0, 255), cv.FILLED)
        return self.landmarks

    def finger_up(self):
        finger = []
        if self.landmarks[self.idtip[0]][1] < self.landmarks[self.idtip[0] - 1][1]:
            finger.append(1)
        else:
            finger.append(0)

        for id in range(1, 5):
            if self.landmarks[self.idtip[id]][2] < self.landmarks[self.idtip[id] - 2][2]:
                finger.append(1)
            else:
                finger.append(0)

        return finger


def main():
    # frame size
    s_width, s_height = 850, 850

    # rectangle size
    x1, x2 = 50, 500
    y1, y2 = 50, 350

    vid = cv.VideoCapture(0)
    vid.set(3, s_width)
    vid.set(4, s_height)
    ptime = 0
    hand = virtual_hand()
    while True:
        rec, img = vid.read()
        c_time = time.time()
        fps = 1 / (c_time - ptime)
        ptime = c_time
        img = cv.flip(img, 1)
        cv.putText(img, f'FPS:{int(fps)}', (15, 30), cv.QT_FONT_NORMAL, 1, (190, 37, 155), 2)
        cv.rectangle(img, (x1, y1), (x2, y2), (250, 0, 0), 3)

        frame1 = hand.tracking(img)
        land = hand.position(frame1)

        if len(land) != 0:
            finger = hand.finger_up()
            if finger[1] == 1 and \
               finger[2] == 0 and \
               finger[3] == 0 and \
               finger[4] == 0:
               cv.circle(frame1, (land[8][1:], land[8][2:]), 15, (255, 0, 0), cv.FILLED)

        cv.imshow("frame", frame1)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    vid.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
