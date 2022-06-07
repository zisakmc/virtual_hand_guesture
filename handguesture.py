import cv2 as cv
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
