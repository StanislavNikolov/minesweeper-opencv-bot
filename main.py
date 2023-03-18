from mss import mss
import sys
import brain
import cv2
import numpy as np
import time

from pynput.mouse import Button, Controller
mouse = Controller()

with mss() as sct:
	monitor = sct.monitors[1]
	print(sct.monitors)

	it = 0
	while True:
		# screen = cv2.imread('00-now.png')
		screen = np.array(sct.grab(monitor))[:,:,:3]
		# cv2.imwrite(f'00-now.png', screen)

		begin = time.time()
		h, what = brain.tell_me_where_to_click(screen, debug=True)
		end = time.time()
		print(f'total {end-begin:.4f}s')

		if h is None:
			print('Nowhere to click')
			continue

		print('target', h, what)
		# continue
		mouse.position = (h.cx, h.cy)
		# time.sleep(0.01)
		cv2.waitKey(10)
		continue

		if what == 'empty':
			mouse.press(Button.left)
			# time.sleep(0.02)
			cv2.waitKey(20)
			mouse.release(Button.left)
			# time.sleep(0.02)
			cv2.waitKey(20)

		if what == 'bomb':
			# mouse.press(Button.left)
			# print('Trying to hold')
			# cv2.waitKey(1000)
			# mouse.release(Button.left)
			mouse.press(Button.right)
			# time.sleep(0.02)
			cv2.waitKey(20)
			mouse.release(Button.right)
			# time.sleep(0.02)
			cv2.waitKey(20)

		it += 1
		print(it)
		# if it > 100: sys.exit(0)