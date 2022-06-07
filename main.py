import cv2 as cv
import mouse
import time
import numpy as np
import handguesture as hg


def main():
    # frame size
    s_width, s_height = 850, 850
    w_screen, h_screen = 1920, 1080

    p_loc_x, p_loc_y = 0, 0
    n_loc_x, n_loc_y = 0, 0
    smoothing_value = 5

    # rectangle size
    x1, x2 = 45, 475
    y1, y2 = 45, 325

    vid = cv.VideoCapture(0)
    vid.set(3, s_width)
    vid.set(4, s_height)
    ptime = 0
    hand = hg.virtual_hand()
    while True:
        rec, img = vid.read()
        c_time = time.time()
        fps = 1 / (c_time - ptime)
        ptime = c_time
        img = cv.flip(img, 1)
        cv.putText(img, f'FPS:{int(fps)}', (15, 30), cv.QT_FONT_NORMAL, 1, (190, 37, 155), 2)

        frame1 = hand.tracking(img)
        land = hand.position(frame1)

        if len(land) != 0:
            x, y = land[8][1:]
            mx, my = land[12][1:]
            rx, ry = land[16][1:]

            finger = hand.finger_up()
            if finger[1] == 1 and \
                    finger[2] == 0 and \
                    finger[3] == 0 and \
                    finger[4] == 0:
                x3 = np.interp(x, (x1, x2), (0, w_screen))
                y3 = np.interp(y, (y1, y2), (0, h_screen))

                n_loc_x = p_loc_x + (x3 - p_loc_x) / smoothing_value
                n_loc_y = p_loc_y + (y3 - p_loc_y) / smoothing_value

                mouse.move(n_loc_x, n_loc_y, absolute=True, duration=0)

                p_loc_x, p_loc_y = n_loc_x, n_loc_y
                cv.circle(frame1, (x, y), 15, (0, 255, 255), cv.FILLED)

            if finger[1] == 1 and \
                    finger[2] == 1 and \
                    finger[3] == 0 and \
                    finger[4] == 0:
                mouse.click()
                cv.circle(frame1, (x, y), 15, (0, 255, 128), cv.FILLED)
                cv.circle(frame1, (mx, my), 15, (102, 255, 128), cv.FILLED)

            if finger[1] == 1 and \
                    finger[2] == 1 and \
                    finger[3] == 1 and \
                    finger[4] == 0:
                mouse.right_click()
                cv.circle(frame1, (x, y), 15, (153, 51, 255), cv.FILLED)
                cv.circle(frame1, (mx, my), 15, (153, 51, 255), cv.FILLED)
                cv.circle(frame1, (rx, ry), 15, (153, 51, 255), cv.FILLED)

        cv.rectangle(frame1, (x1, y1), (x2, y2), (250, 0, 0), 3)

        cv.imshow("frame", frame1)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    vid.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
