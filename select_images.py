import argparse
import json
import shutil
from pathlib import Path
from utils.other_utils import check_dir

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str, default='D:\Download\datasets\舰船\datasets1')
    args = parser.parse_args()

    dir = Path(args.dir)
    chose_dir = dir.parents[0] / 'chose_dir'
    check_dir(chose_dir)
    copy = False
    for p in dir.glob('*.json'):
        with open(p) as f:
            labels_info = json.load(f)
        objs = labels_info['shapes']
        for obj in objs:
            copy = False
            if int(obj['label']) >= 10:
                copy = True
                break
        if copy:
            shutil.copy(p, chose_dir / p.name)
            shutil.copy(dir / (p.stem + '.tif'), chose_dir / (p.stem + '.tif'))
    