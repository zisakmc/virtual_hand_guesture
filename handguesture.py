import cv2 as cv
import mediapipe as mp
from math import hypot
import numpy as np

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
        self.id_tip = [4, 8, 12, 16, 20]

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

        return self.landmarks

    def finger_up(self):
        finger = []
        # thump check up or not
        if self.landmarks[self.id_tip[0]][1] < self.landmarks[self.id_tip[0] - 1][1]:
            finger.append(1)
        else:
            finger.append(0)
        # finger check up or not
        for ids in range(1, 5):
            if self.landmarks[self.id_tip[ids]][2] < self.landmarks[self.id_tip[ids] - 2][2]:
                finger.append(1)
            else:
                finger.append(0)

        return finger

    def distace_index_and_thump(self):
        x1, y1 = self.landmarks[4][1], self.landmarks[4][2]  # thumb
        x2, y2 = self.landmarks[8][1], self.landmarks[8][2]  # index finger
        # creating circle at the tips of thumb and index finger
        hypo = hypot(x2 - x1, y2 - y1) ## calculating hypotenuse
        length = np.interp(hypo, [30, 350], [0, 10]) ## scalling 0 - 10
        return length


    def distace_index_and_middle(self):
        x1, y1 = self.landmarks[12][1], self.landmarks[12][2]  # middle
        x2, y2 = self.landmarks[8][1], self.landmarks[8][2]  # index finger
        # creating circle at the tips of thumb and index finger
        hypo = hypot(x2 - x1, y2 - y1) ## calculating hypotenuse
        length = np.interp(hypo, [30, 350], [0, 10]) ## scalling 0 - 10
        return length

    def distace_middle_and_ring(self):
        x1, y1 = self.landmarks[12][1], self.landmarks[12][2]  # middle finger
        x2, y2 = self.landmarks[16][1], self.landmarks[16][2]  # ring finger
        # creating circle at the tips of thumb and index finger
        hypo = hypot(x2 - x1, y2 - y1) ## calculating hypotenuse
        length = np.interp(hypo, [30, 350], [0, 10]) ## scalling 0 - 10
        return length

    def distace_ring_and_pinky(self):
        x1, y1 = self.landmarks[15][1], self.landmarks[15][2]  # ring finger
        x2, y2 = self.landmarks[20][1], self.landmarks[20][2]  # pinky finger
        # creating circle at the tips of thumb and index finger
        hypo = hypot(x2 - x1, y2 - y1) ## calculating hypotenuse
        length = np.interp(hypo, [30, 350], [0, 10]) ## scalling 0 - 10
        return length
