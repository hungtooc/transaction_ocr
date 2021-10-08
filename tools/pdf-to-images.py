import glob
import ntpath

import numpy as np
import cv2
import io
import os
from pathlib import Path
from pdf2image import convert_from_path, convert_from_bytes, pdfinfo_from_bytes

if __name__ == '__main__':

    pdf_dir = "/home/hungtooc/Documents/SAOKE/Thuy-Tien/input/TÀI KHOẢN XXX746 (Pass_ Vcbsaoke@2021)/TỪ 13.10.20 ĐẾN 23.11.20"
    output_dir = "../data/data-raw/TỪ 13.10.20 ĐẾN 23.11.20"
    pdf_password = "Vcbsaoke@2021"
    cv2.namedWindow("page", cv2.WINDOW_NORMAL)
    for index, pdf_path in enumerate(sorted(glob.glob(f"{pdf_dir}/*.pdf"))[:1]):
        print(f"(None) processing {pdf_path}...")
        sub_output_dir = f"{output_dir}/{ntpath.basename(pdf_path)}/"
        Path(sub_output_dir).mkdir(parents=True, exist_ok=True)
        info = pdfinfo_from_bytes(open(pdf_path, "rb").read(), userpw=pdf_password, poppler_path=None)
        # to_page_no = 18107
        from_page_no = 1
        # to_page_no = info['Pages']  # max page no
        to_page_no = 10
        add_page_no = 0
        print(f"maxPages: {to_page_no}")
        for page in range(from_page_no, to_page_no + 1, 50):
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
