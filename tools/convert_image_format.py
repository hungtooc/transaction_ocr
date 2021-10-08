import numpy as np
import glob
import cv2
import ntpath
import shutil
import os
from PIL import Image
# from PIL import Pillow
import pyheif


def work_with_image(file_path):
    heif_file = pyheif.read(file_path)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    image = np.array(image)
    # Convert RGB to BGR
    image = image[:, :, ::-1].copy()
    return image


if __name__ == '__main__':
    image_dir = "/home/hungtooc/Downloads/SAOKE_tranthanh/drive-download-20210907T104436Z-001"
    for image_path in glob.glob(f"{image_dir}/*/*.HEIC"):
        image = work_with_image(image_path)
        cv2.imwrite(image_path.replace('.HEIC', '.jpg'), image)
        # cv2.imshow("image", image)
        # cv2.waitKey(0)
