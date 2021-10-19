import pathlib
import hashlib
import json
import glob
import ntpath
import cv2
import numpy as np
import shutil
import argparse
import sys
from tqdm import tqdm
import os
from pathlib import Path
from tqdm import tqdm

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


class Annotation:
    def __init__(self, description, vertices):
        self.description = description
        self.vertices = vertices


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--respone-dir', type=str, default=ROOT / 'data/api-respone/TÀI KHOẢN XXX746 (Pass_ Vcbsaoke@2021)/TỪ 13.10.20 ĐẾN 23.11.20',
                        help='dir to api respone')
    parser.add_argument('-a', '--output-annotation', type=str, default='data/dataset/annotations.txt', help='path to save annotation file')
    parser.add_argument('-i', '--output-image-dir', type=str, default='data/dataset/images', help='path to save annotation file')
    opt = parser.parse_args()
    return opt


def sha1_file(f):
    return hashlib.sha1(f).hexdigest()


if __name__ == '__main__':
    opt = parse_opt()
    output_image_dir = opt.output_image_dir
    output_annotation_path = opt.output_annotation
    respone_dir = opt.respone_dir
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    for sub_respone_dir in glob.glob(f"{respone_dir}/*/"):
        print(sub_respone_dir)
        foutput_annotation = open(output_annotation_path, "a", encoding='utf8')
        labels = []
        sub_dir_image = f"{output_image_dir}/{sub_respone_dir.split('/')[-2]}"
        Path(sub_dir_image).mkdir(parents=True, exist_ok=True)
        for json_path in tqdm(sorted(glob.glob(f"{sub_respone_dir}/*.json"), key=lambda k: int(ntpath.basename(k).split('.')[0].replace('page_', '')))):
            sub_sub_dir_image = f"{sub_dir_image}/{ntpath.basename(json_path).replace('.json','')}"
            Path(sub_sub_dir_image).mkdir(parents=True, exist_ok=True)
            with open(json_path, encoding='utf8') as json_file:
                data = json.load(json_file)
                image_path = data['image_path']
                data_respones = []
                for data_respone in data['respone']:
                    data_respones.append(Annotation(data_respone['desc'], data_respone['vertices']))
                image = cv2.imread(image_path)
                for index, data_respone in enumerate(data_respones):
                    # cv2.polylines(image, np.array(data_respone.vertices), True, (0, 255, 0), 1)
                    roi = image[np.min(data_respone.vertices, 1)[0][1]:np.max(data_respone.vertices, 1)[0][1],
                          np.min(data_respone.vertices, 1)[0][0]:np.max(data_respone.vertices, 1)[0][0]]
                    if roi is not None:
                        # img_str = cv2.imencode('.jpg', roi)[1].tobytes()
                        # filename = f"{ntpath.basename(image_path).replace('.jpg', '')}_{sha1_file(img_str)}.jpg"
                        filename = f"{ntpath.basename(image_path).replace('.jpg', f'_{index}.jpg')}"
                        cv2.imwrite(f"{sub_sub_dir_image}/{filename}", roi)
                        labels.append(f"{sub_respone_dir.split('/')[-2]}/{ntpath.basename(json_path).replace('.json','')}/{filename} {data_respone.description}")
                    # cv2.imshow("image", image)
                    # cv2.waitKey(10)
            foutput_annotation.write("\n".join(labels) + "\n")
