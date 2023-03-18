import math
from pathlib import Path
from typing import Iterable
from dataclasses import dataclass
import cv2
import numpy as np
import brain.cell_type

model = brain.cell_type.make_model(Path('train'))

@dataclass
class Hex:
    type: str
    q: int
    r: int
    cx: int
    cy: int


def find_possible_hex_contours(screen, debug=False) -> list:
    imgray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    # ret, thresh = cv2.threshold(imgray, 54, 255, 0)
    ret, thresh = cv2.threshold(imgray, 40, 255, 0)
    
    # DEBUG
    # cv2.imwrite('01-thresh.png', thresh)
    if debug: cv2.imshow('thresh', thresh)

    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(thresh, kernel, iterations=1)

    # if debug: cv2.imwrite('02-erosion.png', erosion)

    contours, hierarchy = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hex_contours = []
    for contour in contours:
        if cv2.isContourConvex(contour):
            continue

        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 6:
            hex_contours.append(approx)

    return hex_contours


def find_closest(rects: Iterable[tuple[int,int,int,int]], tx: float, ty: float):
    min_dist_sq = 999999999999
    closest = None
    for r in rects:
        cx = r[0] + r[2]//2
        cy = r[1] + r[3]//2
        dist_sq = (cx-tx)**2 + (cy-ty)**2
        if dist_sq < min_dist_sq:
            min_dist_sq = dist_sq
            closest = r

    return closest, math.sqrt(min_dist_sq)


def calc_grid_props(screen, contours):
    rects = [cv2.boundingRect(c) for c in contours]
    centermost, _ = find_closest(rects, screen.shape[1]//2, screen.shape[0]//2)
    rects.remove(centermost)
    _, dist  = find_closest(rects, centermost[0]+centermost[2]//2, centermost[1]+centermost[3]//2)
    return centermost, dist


def make_hex(close_hex: Hex, new: tuple[int, int, int, int]):
    angle = math.atan2(new[1]+new[3]//2 - close_hex.cy, new[0]+new[2]//2 - close_hex.cx)
    def mod(a, n): return (a % n + n) % n
    def ang_close_to(ang, target):
        delta = target - ang
        delta = mod(delta + math.pi, math.tau) - math.pi
        return -0.1 <= delta <= 0.1

    q, r = close_hex.q, close_hex.r
    nq, nr = None, None
    
    if ang_close_to(angle,   0/180*math.pi): nq, nr = q+1, r  
    if ang_close_to(angle,  60/180*math.pi): nq, nr = q  , r+1
    if ang_close_to(angle, 120/180*math.pi): nq, nr = q-1, r+1
    if ang_close_to(angle, 180/180*math.pi): nq, nr = q-1, r  
    if ang_close_to(angle, 240/180*math.pi): nq, nr = q  , r-1
    if ang_close_to(angle, 300/180*math.pi): nq, nr = q+1, r-1

    if nq is None: return None

    return Hex(None, nq, nr, new[0]+new[2]//2, new[1]+new[3]//2) 


def get_label(screen, x:int, y:int, w:int, h:int):
    qw = w // 4
    qh = h // 4
    cut = screen[y+qh:y+h-qh,x+qw:x+w-qw]
    result = brain.cell_type.run_model(model, cut)
    return brain.cell_type.label_int2str[int(result)]


def find_hexagons(screen, contours):
    centermost, hex_dist = calc_grid_props(screen, contours)

    rects = [cv2.boundingRect(c) for c in contours]
    rects.remove(centermost)

    discovered = [ Hex(None, 0, 0, centermost[0]+centermost[2]//2, centermost[1]+centermost[3]//2) ]
    discovered[0].type = get_label(screen, *centermost)

    curr_i = 0
    while curr_i < len(discovered):
        curr = discovered[curr_i]
        closest, d = find_closest(rects, curr.cx, curr.cy)

        if hex_dist * 0.95 <= d <= hex_dist * 1.05:
            h = make_hex(curr, closest)
            # print(f'{new_hex=}')
            if h is not None:
                h.type = get_label(screen, *closest)
                discovered.append(h)
                rects.remove(closest)
                continue

        curr_i += 1

    return discovered