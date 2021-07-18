import os 

import glob
import json
import math
import pprint
import argparse
import numpy as np
from shapely.geometry import *
from tqdm import tqdm

def judge_direction(p1, p2, p3):
    f_p = eval('p{}'.format(str([p1[1], p2[1]].index(max(p1[1], p2[1])) + 1)))
    f_b = eval('p{}'.format(str([p1[1], p2[1]].index(min(p1[1], p2[1])) + 1)))
    s = (f_p[0] - p3[0]) * (f_b[1] - p3[1]) - (f_p[1] - p3[1]) * (f_b[0] - p3[0])
    direction = "left" if s > 0 else "right" if s < 0 else s
    return direction

def get_label(points, objs):
    p1 = Polygon(points)
    iou = 0
    max_index = []
    for i, obj in enumerate(objs):
        if obj['label'] != 'null-label':
            p2 = Polygon(obj['points'])
            t_iou = p1.intersection(p2).area / p1.union(p2).area
            if t_iou > iou:
                iou = t_iou
                max_index.append(1)
                continue
        max_index.append(0)
    objs[(len(objs) - max_index[::-1].index(1) - 1)]['points'] = points

def check_dir(p):
    if os.path.exists(p):
        print(f"already exists {p}")
    else:
        os.mkdir(p)
        print(f"the dir don't exist, create{p}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default=r'D:\Download\飞机数据集标注数据及说明\rcf_annotations\json_annotations\*.json')
    parser.add_argument('--new_path', type=str, default='')
    args = parser.parse_args()
    assert args.path!='', "the annotations dir can not be empty"
    if args.new_path == '':
        args.new_path = os.path.join(os.path.split(args.path)[0], '..', 'new_annotations')
    out_boundary = []
    PATH = args.path
    NEW_PATH = args.new_path
    check_dir(NEW_PATH)
    for p in tqdm(glob.glob(PATH)):
        with open(p, 'rb') as fr:
            label_info = json.load(fr)
        fr.close()
        objs = label_info['shapes']
        height = label_info['imageHeight']
        width = label_info['imageWidth']
        new_objs = []
        # get rotated bbox
        for obj in objs:
            if obj['label'] == 'null-label':
                points = obj['points']
                line1 = LineString(points[:2])
                point2 = Point(points[2])
                point3 = Point(points[3])
                d1 = point2.distance(line1)
                d2 = point3.distance(line1)
                line2 = line1.parallel_offset(d1, side='right')
                line3 = line1.parallel_offset(d2, side='left')
                side2 = judge_direction(points[0], points[1], points[2]) # judge the direction of the parallel line
                side2_ = judge_direction(points[0], points[1], list(line2.coords[0])) 
                if side2 != side2_:
                    line2 = line1.parallel_offset(d1, side='left')
                    line3 = line1.parallel_offset(d2, side='right')
                new_points = [list(line2.coords[0]), list(line2.coords[1]), list(line3.coords[0]), list(line3.coords[1])]
                get_label(new_points, objs)
        # get not null_label information
        for obj in objs:
            points = obj['points']
            ps = np.array(points)
            if not ((0 <= ps[:, 0]) & (ps[:, 0] <= width - 1) & (0 <= ps[:, 1]) & (ps[:, 1] <= height - 1)).all():
                out_boundary.append(label_info['imagePath'])
            if obj['label'] != 'null-label':
                new_objs.append(obj)

        label_info['shapes'] = new_objs

        new_p = os.path.join(NEW_PATH, os.path.split(p)[1])
        with open(new_p, 'w') as fw:
            json.dump(label_info, fw, indent=4)
        fw.close()
with open(os.path.join(NEW_PATH, 'out_boundary.txt'), 'w') as fw:
    fw.write(str(out_boundary))
fw.close()


        
    
    