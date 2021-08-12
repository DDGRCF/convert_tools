import logging
from pathlib import Path
from shapely.geometry import *

logger = logging.getLogger(__name__)
__all__ = ["judge_direction", "get_label", "check_dir", "set_logging"]

def set_logging():
    logging.basicConfig(format="%(message)s", level=logging.INFO)

def judge_direction(p1, p2, p3):
    f_p = eval('p{}'.format(str([p1[1], p2[1]].index(max(p1[1], p2[1])) + 1)))
    f_b = eval('p{}'.format(str([p1[1], p2[1]].index(min(p1[1], p2[1])) + 1)))
    s = (f_p[0] - p3[0]) * (f_b[1] - p3[1]) - (f_p[1] - p3[1]) * (f_b[0] - p3[0])
    direction = "left" if s > 0 else "right" if s < 0 else s
    return direction

def get_label(points, objs, temp_label):
    p1 = Polygon(points)
    iou = 0
    max_index = []
    for _, obj in enumerate(objs):
        if obj['label'] != temp_label:
            p2 = Polygon(obj['points'])
            t_iou = p1.intersection(p2).area / p1.union(p2).area
            if t_iou > iou:
                iou = t_iou
                max_index.append(1)
                continue
        max_index.append(0)
    objs[(len(objs) - max_index[::-1].index(1) - 1)]['points'] = points

def check_dir(p):
    if p.is_dir():
        logger.info(f"already exists {p}")
    else:
        p.mkdir(parents=True)
        logger.info(f"create dir-{p}")


