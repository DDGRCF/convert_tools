import argparse
import json
from pathlib import Path
from tqdm import tqdm
from prettytable import PrettyTable


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str, default=r'F:\Datasets\new_annotations')
    parser.add_argument('--adjust', action='store_true')
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

        for obj in objs:
            label = obj['label']
            if label in class_num:
                class_num[label] += 1
            else:
                class_num[label] = 1
            if args.adjust:
                if label == '20':
                    obj['label'] = '23'
                elif label == '23':
                    obj['label'] = '20'
        if args.adjust:
            with open(p, 'w') as fw:
                json.dump(label_info, fw, indent=4)
    for k in sorted(class_num):
        table.add_row([k, class_num[k]])
    print(table)
        