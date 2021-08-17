import argparse
import json
from pathlib import Path
from tqdm import tqdm
from prettytable import PrettyTable


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str, default=r'F:\Datasets\new_annotations')
    parser.add_argument('--labels_adjust', action='store_true')
    parser.add_argument('--paths_adjust', action='store_true')
    parser.add_argument('--suffix', type=str, default="tif")
    args = parser.parse_args()

    dir = Path(args.dir)
    num = sum(1 for _ in dir.glob("*.json"))
    class_num = {}
    table = PrettyTable(['class', 'num'])
    for p in tqdm(dir.glob("*.json"), desc='Processing', total=num):
        p = dir / p
        with open(p, 'rb') as fr:
            label_info = json.load(fr)
        objs = label_info['shapes']
        if args.paths_adjust:
            i_p = p.stem + "." + args.suffix
            label_info['imagePath'] = i_p
        for obj in objs:
            label = obj['label']
            if args.paths_adjust:
                obj['group_id'] = None
            if label in class_num:
                class_num[label] += 1
            else:
                class_num[label] = 1
            if args.labels_adjust:
                if label == '20':
                    obj['label'] = '23'
                elif label == '23':
                    obj['label'] = '20'
        if args.labels_adjust or args.paths_adjust:
            with open(p, 'w') as fw:
                json.dump(label_info, fw, indent=4)
    for k in sorted(class_num):
        table.add_row([k, class_num[k]])
    print(table)
        