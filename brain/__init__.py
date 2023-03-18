from brain import grid_builder, grid_solver
import math
import numpy as np
import cv2
import time

cv2.namedWindow("thresh", 0);
cv2.moveWindow("thresh", 2560, 0)
cv2.resizeWindow("thresh", 500, 300)

cv2.namedWindow("contours", 0);
cv2.moveWindow("contours", 2560, 0)
cv2.resizeWindow("contours", 500, 300)

cv2.namedWindow("brain", 0);
cv2.moveWindow("brain", 2560, 250)
cv2.resizeWindow("brain", 800, 800)

def tell_me_where_to_click(screen, debug=False):
	a = time.time()
	contours = grid_builder.find_possible_hex_contours(screen, debug)

	if debug:
		screen_with_contours = screen.copy()
		cv2.drawContours(screen_with_contours, contours, -1, (0,255,0), 3)

		for idx, c in enumerate(contours):
			x,y,w,h = cv2.boundingRect(c)
			qw = w // 4
			qh = h // 4
			cut = screen[y+qh:y+h-qh,x+qw:x+w-qw]

			cv2.circle(screen_with_contours, (x+w//2, y+h//2), 3, (255, 255, 255), -1)
			# cv2.rectangle(screen_with_contours,(x+qw,y+qh),(x+w-qw,y+h-qh),(0,255,0),2)
			# cv2.imwrite(f"05-cut-{idx}.png", cut)

		#cv2.imwrite("03-hexagon contours.png", screen_with_contours)
		cv2.imshow('contours', screen_with_contours)

	b = time.time()


	hexagons = grid_builder.find_hexagons(screen, contours)
	if debug:
		## Debug - render the hexagons
		def hex_to_pixel(q, r, size):
			x = size * (math.sqrt(3) * q + math.sqrt(3)/2 * r)
			y = size * (3./2 * r)
			return (x, y)
		rdr = np.zeros((2500, 2500, 3), dtype=np.uint8)

		def txt(text, x, y, color):
			cv2.putText(rdr, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

		for h in hexagons:
			rdr_x, rdr_y = hex_to_pixel(h.q, h.r, 40)
			pos = (int(rdr_x) + rdr.shape[1]//2, int(rdr_y) + rdr.shape[0]//2)
			type2color = {
				'nobody': (  50,  50,  50, ),
				'other':  (  50,  50, 250, ),
				'inside': ( 140,  80,  80, ),
				'flag':   (  40, 250,  20, ),
				'border': ( 120, 230, 120, ),
			}
			color = type2color.get(h.type, (255, 255, 255))
			# print(h)
			cv2.circle(rdr, pos, 33, color, 2)
			txt(h.type[0], pos[0] - 4, pos[1] - 12, color)
			txt(f'{h.q} {h.r}', pos[0] - 25, pos[1] + 8, color)
		# cv2.imwrite('04-recovered hexagons.png', rdr)
	c = time.time()


	border_hexagons_with_results = grid_solver.reveal_cells(hexagons)
	if debug:
		## Debug - render the results
		for h, result in border_hexagons_with_results:
			rdr_x, rdr_y = hex_to_pixel(h.q, h.r, 40)
			pos = (int(rdr_x) + rdr.shape[1]//2, int(rdr_y) + rdr.shape[0]//2)
			result_text = {None:'=?', 0:'=ok', 1:'=f', 2:'=all'}[result]
			txt(result_text, pos[0] - 10, pos[1] + 20, (107,183,189))

		cv2.imshow("brain", rdr)

	d = time.time()

	print(f'contours:      {b-a:.4f}s')
	print(f'find hexagons: {c-b:.4f}s')
	print(f'z3:            {d-c:.4f}s')

	# Prioritize
	for h, result in border_hexagons_with_results:
		if result == 1: return h, 'bomb'
	for h, result in border_hexagons_with_results:
		if result == 0: return h, 'empty'


	return None, '?'
