import os
import cv2 as cv
import mouse
import time
import numpy as np
import handguesture as hg
import pyautogui as pg
import mode
import threading

def main():
    # frame size
    s_width, s_height = 850, 850
    w_screen, h_screen = pg.size()

    p_loc_x, p_loc_y = 0, 0
    n_loc_x, n_loc_y = 0, 0
    smoothing_value = 9

    # rectangle size
    x1, x2 = 45, 475
    y1, y2 = 45, 325

    vid = cv.VideoCapture(0)
    vid.set(3, s_width)
    vid.set(4, s_height)
    ptime = 0
    hand = hg.virtual_hand()

    mode = 1 # 0 - interactive mode 1 - luncher mode
    pg.FAILSAFE=False
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
            lx, ly = land[20][1:]
            tx, ty = land[4][1:]
            finger = hand.finger_up()
            if (mode == 1):
                if finger[1] == 1 and \
                        finger[2] == 0 and \
                        finger[3] == 0 and \
                        finger[4] == 0:
                    x3 = np.interp(x, (x1, x2), (0, w_screen))
                    y3 = np.interp(y, (y1, y2), (0, h_screen))

                    n_loc_x = p_loc_x + (x3 - p_loc_x) / smoothing_value
                    n_loc_y = p_loc_y + (y3 - p_loc_y) / smoothing_value
                    # pg.moveTo(n_loc_x, n_loc_y)
                    mouse.move(n_loc_x, n_loc_y, absolute=True, duration=0)

                    p_loc_x, p_loc_y = n_loc_x, n_loc_y
                    cv.circle(frame1, (x, y), 15, (0, 255, 255), cv.FILLED)

                if finger[1] == 1 and \
                        finger[2] == 1 and \
                        finger[3] == 0 and \
                        finger[4] == 0 and \
                        hand.distace_index_and_middle()==0:
                    # mouse.click()
                    pg.click()
                    cv.circle(frame1, (x, y), 15, (0, 255, 128), cv.FILLED)
                    cv.circle(frame1, (mx, my), 15, (102, 255, 128), cv.FILLED)

                if finger[1] == 1 and \
                        finger[2] == 1 and \
                        finger[3] == 1 and \
                        finger[4] == 0 and \
                        hand.distace_index_and_middle()==0 and \
                        hand.distace_middle_and_ring() <= 5:
                    # mouse.right_click()

                    time.sleep(0.5)
                    pg.rightClick()

                    cv.circle(frame1, (x, y), 15, (153, 51, 255), cv.FILLED)
                    cv.circle(frame1, (mx, my), 15, (153, 51, 255), cv.FILLED)
                    cv.circle(frame1, (rx, ry), 15, (153, 51, 255), cv.FILLED)
                if finger[1] == 0 and \
                        finger[2] == 0 and \
                        finger[3] == 0 and \
                        finger[4] == 1:
                    pg.scroll(-20, _pause=0)
                    cv.circle(frame1, (lx, ly), 15, (102, 255, 128), cv.FILLED)
                if finger[0] == 1 and \
                        finger[1] == 0 and \
                        finger[2] == 0 and \
                        finger[3] == 0 and \
                        finger[4] == 0:
                    pg.scroll(20, _pause=0)
                    cv.circle(frame1, (tx, ty), 15, (102, 255, 128), cv.FILLED)

                if(hand.distace_index_and_thump() ==0 and \
                        hand.distace_index_and_middle() == 0 and \
                        finger[1] == 1 and \
                        finger[2] == 0 and \
                        finger[3] == 0 and \
                        finger[4] == 0):

                    x3 = np.interp(x, (x1, x2), (0, w_screen))
                    y3 = np.interp(y, (y1, y2), (0, h_screen))

                    n_loc_x = p_loc_x + (x3 - p_loc_x) / smoothing_value
                    n_loc_y = p_loc_y + (y3 - p_loc_y) / smoothing_value
                    # pg.moveTo(n_loc_x, n_loc_y)
                    pg.drag(n_loc_x, n_loc_y, button='left')
                    p_loc_x, p_loc_y = n_loc_x, n_loc_y

                if finger[1] == 1 and \
                        finger[2] == 0 and \
                        finger[3] == 0 and \
                        finger[4] == 1:
                    if pg.confirm(text='Change Mode', title='MODE', buttons=['OK', 'Cancel']) == 'OK':
                        mode = 0
                    else:
                        mode = 1
            else:

                if finger[1] == 1 and \
                        finger[2] == 1 and \
                        finger[3] == 0 and \
                        finger[4] == 0 and \
                        hand.distace_index_and_middle() == 0:
                    #time.sleep(3)
                    print('second command')
                    mode=1
                    os.system('cmd /C taskkill /f /im "calc.exe" /t')
                    os.system('C:\\Windows\\System32\\calc.exe')

                if finger[1] == 1 and \
                        finger[2] == 1 and \
                        finger[3] == 1 and \
                        finger[4] == 0 and \
                        hand.distace_index_and_middle() == 0 \
                        and hand.distace_middle_and_ring() <= 5:
                    #time.sleep(3)
                    #os.system('cmd /C taskkill /f /im "notepad.exe" /t')
                    os.startfile(r"C:\\Windows\\System32\\notepad.exe")

                    mode = 1

                if finger[1] == 1 and \
                        finger[2] == 1 and \
                        finger[3] == 1 and \
                        finger[4] == 1 and \
                        hand.distace_index_and_middle() == 0 \
                        and hand.distace_middle_and_ring() <= 5 \
                        and hand.distace_ring_and_pinky() <= 7:
                    # time.sleep(3)
                    #mode = 1
                    #os.system('cmd /C taskkill /f /im "brave.exe" /t')
                    os.startfile(r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe")
                    mode = 1

        cv.rectangle(frame1, (x1, y1), (x2, y2), (250, 0, 0), 3)

        cv.imshow("frame", frame1)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    vid.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
