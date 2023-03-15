from mss import mss
import sys
import brain
import cv2


sct = mss()
def capture_screen():
    # with mss() as sct:
    # 	# print(sct.monitors)
    # 	monitor = sct.monitors[0]
    # 	import time
    # 	time.sleep(2)
    #	sct.shot()
    # 	# screen = np.array(sct.grab(sct.monitors[0]))
    pass


if __name__ == '__main__':
    screen = cv2.imread('00-02-screenshot.png')

    pixel_x, pixel_y = brain.tell_me_where_to_click(screen)
    # hand.click_at(pixel_x, pixel_y)

    sys.exit(0)

    cv2.imshow("cnt", screen)

    while True:
        if cv2.waitKey(25) == ord("q"):
            cv2.destroyAllWindows()
            break
