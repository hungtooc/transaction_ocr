import glob
import ntpath

import numpy as np
import cv2
import io
import os
from pathlib import Path
from pdf2image import convert_from_path, convert_from_bytes, pdfinfo_from_bytes
import argparse
import sys
from tqdm import tqdm
FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf-dir', type=str, default=ROOT / 'data/input', help='dir to pdf files')
    parser.add_argument('--output-dir', type=str, default=ROOT / 'data/raw-image/TỪ 13.10.20 ĐẾN 23.11.20', help='dir to save images')
    parser.add_argument('--pdf-password', type=str, default=None, help='pdf password')
    parser.add_argument('--from-page-no', type=int, default=1, help='extra image from page')
    parser.add_argument('--to-page-no', type=int, default=-1, help='extra image to page')
    parser.add_argument('--fix-page-number', type=int, default=0, help='fix page number (page_no += fix_page_number)')
    opt = parser.parse_args()
    return opt


if __name__ == '__main__':
    opt = parse_opt()
    pdf_dir = opt.pdf_dir
    output_dir = opt.output_dir
    pdf_password = opt.pdf_password
    from_page_no = opt.from_page_no
    to_page_no = opt.to_page_no
    add_page_no = opt.fix_page_number
    for index, pdf_path in enumerate(sorted(glob.glob(f"{pdf_dir}/*.pdf"))[:1]):
        sub_output_dir = f"{output_dir}/{ntpath.basename(pdf_path)}/"
        Path(sub_output_dir).mkdir(parents=True, exist_ok=True)
        info = pdfinfo_from_bytes(open(pdf_path, "rb").read(), userpw=pdf_password, poppler_path=None)
        to_page_no = to_page_no if to_page_no != -1 else info['Pages']
        print(f"processing {ntpath.basename(pdf_path)} from page {from_page_no} to page {to_page_no}, with appending page number {add_page_no}")
        for page in tqdm(range(from_page_no, to_page_no + 1, 50)):
            images = convert_from_bytes(open(pdf_path, "rb").read(), first_page=page, last_page=min(page + 49, to_page_no), userpw=pdf_password)
            print(f"from page {page} to {min(page + 49, to_page_no)}, len = {len(images)}")
            for index, image in enumerate(images):
                image = np.array(image)
                # Convert RGB to BGR
                image = image[:, :, ::-1]
                cv2.imwrite(f"{sub_output_dir}/page_{add_page_no + page + index}.jpg", image)
                print(f'- page {add_page_no + page + index}')
                # cv2.imshow("page", image)
                # cv2.waitKey(0)
