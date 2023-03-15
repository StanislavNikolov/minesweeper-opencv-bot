from brain import frontal_lobe, occipital_lobe

def tell_me_where_to_click(screen):
    contours = occipital_lobe.find_possible_hex_contours(screen, debug=True)
    ## Debug
    # screen_with_contours = screen.copy()
    # cv2.drawContours(screen_with_contours, contours, -1, (0,255,0), 3)
    # cv2.imwrite("03-hexagon contours.png", screen_with_contours)
    # for idx, c in enumerate(contours):
    # 	x,y,w,h = cv2.boundingRect(c)
    # 	qw = w // 4
    # 	qh = h // 4
    # 	cut = screen[y+qh:y+h-qh,x+qw:x+w-qw]
    # 	result = train.run_model(model, cut)
    # 	txt = train.label_int2str[int(result)]

    # 	cv2.putText(
    # 		img=screen_with_contours,
    #       	text=txt[0],
    # 	 	org=(x+w//2, y+h//2),
    # 		fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    # 		fontScale=1,
    # 		color=(255,255,255),
    # 		thickness=2,
    # 		lineType=2
    # 	)

    # 	cv2.circle(screen_with_contours, (x+w//2, y+h//2), 7, (255, 255, 255), -1)
    # 	# cv2.rectangle(screen_with_contours,(x+qw,y+qh),(x+w-qw,y+h-qh),(0,255,0),2)
    # 	# cv2.imwrite(f"05-cut-{idx}.png", cut)
    # cv2.imwrite("04-hexagon center.png", screen_with_contours)


    hexagons = occipital_lobe.find_hexagons(screen, contours)
    ## Debug - render the hexagons
    # def hex_to_pixel(q, r, size):
    #     x = size * (math.sqrt(3) * q + math.sqrt(3)/2 * r)
    #     y = size * (3./2 * r)
    #     return (x, y)
    # rdr = np.zeros((2000, 2000, 3), dtype=np.uint8)
    # for h in hexagons:
    #     rdr_x, rdr_y = hex_to_pixel(h.q, h.r, 20)
    #     pos = (int(rdr_x) + 1000, int(rdr_y) + 1000)
    #     type2color = {
    #         'nobody': (  50,  50,  50, ),
    #         'red':    (  50,  50, 250, ),
    #         'inside': ( 140,  80,  80, ),
    #         'flag':   (  40, 250,  20, ),
    #         'border': ( 120, 230, 120, ),
    #     }
    #     color = type2color.get(h.type, (255, 255, 255))
    #     # print(h)
    #     cv2.circle(rdr, pos, 15, color, 2)
    #     cv2.putText(rdr, h.type[0], (pos[0] - 4, pos[1] + 3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    # cv2.imwrite('05-recovered hexagons.png', rdr)


    # Turn the array of hexagons into a z3 equation
    frontal_lobe.reveal_cells(hexagons)

    return (0, 0)
