import datetime
import glob
import math
import ntpath
from pathlib import Path

import cv2
import imutils
import numpy as np
from google.cloud import vision

from ocr.google_ocr import googleocr, drawtextpoly
from utils.data_processing import append_processed, save_content, save_respone
from utils.image_processing import ObjectMatching
from utils.mathematics import istextboxinrange, rotate
from utils.vector import ang

if __name__ == '__main__':
    image_dir = "data/data-raw/TỪ 13.10.20 ĐẾN 23.11.20"
    output_respone_dir = "data/api-respone/TÀI KHOẢN XXX746 (Pass_ Vcbsaoke@2021)/TỪ 13.10.20 ĐẾN 23.11.20"
    log_processed_file = "data/processed_page.txt"
    image_header = cv2.imread("utils/images/template_header.jpg")
    image_footer = cv2.imread("utils/images/template_footer.jpg")
    content_dir = "data/content/TÀI KHOẢN XXX746 (Pass_ Vcbsaoke@2021)/TỪ 13.10.20 ĐẾN 23.11.20"
    content_header = ['TNX Date', 'Doc No', 'Debit', 'Credit', 'Balance', 'Transaction in detail', '(note)']
    detector = cv2.SIFT_create()
    client = vision.ImageAnnotatorClient()
    # config content
    header_columns = [0.0000, 0.1463, 0.3089, 0.4815, 0.6555, 1.0000]  # define size-rate of each columm
    date_format = "%d/%m/%Y"
    # cv2.namedWindow(f"rotated_image", cv2.WINDOW_NORMAL)
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    log_processed = [path for path in open(log_processed_file).read().split("\n")]
    for sub_image_dir in sorted(glob.glob(f"{image_dir}/*/"), key=lambda k: int(k.split("/")[-2].split('.')[0])):
        print(sub_image_dir)
        sub_output_respone_dir = f"{output_respone_dir}/{sub_image_dir.split('/')[-2]}"
        sub_content_dir = f"{content_dir}/{sub_image_dir.split('/')[-2]}"
        Path(sub_output_respone_dir).mkdir(parents=True, exist_ok=True)
        Path(sub_content_dir).mkdir(parents=True, exist_ok=True)
        for image_path in sorted(glob.glob(f"{sub_image_dir}*.jpg"), key=lambda k: int(ntpath.basename(k).split("_")[-1].replace(".jpg", ""))):
            if image_path in log_processed:
                print(f"Skip processed {ntpath.basename(image_path)}")
                continue
            print(image_path)
            ## margin image (rotated_image)
            image = cv2.imread(image_path)

            # cv2.imshow("image", image)
            _, corners_header = ObjectMatching(image, image_header, detector)
            kp, corners_footer = ObjectMatching(image, image_footer, detector)

            # cv2.circle(image, corners_footer[2], 4, (0, 0, 0), -1)  # for debug
            rotate_angle = ang(corners_header[:2])
            # image = cv2.drawKeypoints(image, kp, None, color=(0, 255, 0), flags=0)  # for debug

            print("re-rotate (angle):", rotate_angle)
            rotated_image = imutils.rotate_bound(image, rotate_angle)
            cv2.imwrite(image_path, rotated_image)  # todo: should optimize

            (h, w) = image.shape[:2]
            (cX, cY) = (w / 2, h / 2)
            bounding = np.array([rotate((cX, cY), (0, 0), math.radians(rotate_angle)),
                                 rotate((cX, cY), (0, image.shape[1]), math.radians(rotate_angle)),
                                 rotate((cX, cY), (image.shape[0], 0), math.radians(rotate_angle))])
            align_bounding = abs(np.amin(bounding, axis=0).astype(int))
            corners_header = np.array([rotate((cX, cY), point, math.radians(rotate_angle)) for point in corners_header]).astype(np.int32)
            corners_footer = np.array([rotate((cX, cY), point, math.radians(rotate_angle)) for point in corners_footer]).astype(np.int32)
            corners_header += align_bounding
            corners_footer += align_bounding

            # Step 4: clean image
            # cv2.fillPoly(image, [corners_footer.reshape((-1, 1, 2))], (255, 255, 255))
            rotated_image[:corners_header[0][1]] = (255, 255, 255)
            rotated_image[:, :corners_header[0][0]] = (255, 255, 255)
            rotated_image[:, corners_header[1][0]:] = (255, 255, 255)

            cv2.imwrite("data/temp_query.jpg", rotated_image)  # recommend saving image to SSD disk todo: should optimize

            texts = googleocr("data/temp_query.jpg", client, issort=False)  # todo: you much have an account to call googleocr() fubction https://cloud.google.com/vision/docs/ocr

            save_respone(texts[1:], image_path,
                         f"{sub_output_respone_dir}/{ntpath.basename(image_path).replace('.jpg', '.json')}")  # save respone, then you can generate dataset for text-recognization.

            transactions = []
            for text in texts[1:]:
                text_string = text.description
                try:
                    # for simple, we define each transaction has a datetime string. todo: should optimize
                    # check if text_string is datetime string
                    datetime.datetime.strptime(text_string, date_format)
                    transactions.append(text)
                    ## for debug
                    # cv2.line(rotated_image, [text.bounding_poly.vertices[0].x, text.bounding_poly.vertices[0].y],
                    #          [rotated_image.shape[1], text.bounding_poly.vertices[0].y],
                    #          (0, 0, 255), 3)
                    # cv2.circle(rotated_image, [text.bounding_poly.vertices[0].x, text.bounding_poly.vertices[0].y], 7, (255, 0, 0), -1)
                    drawtextpoly(rotated_image, text, show_label=False, text_color=(0, 0, 0), poly_thickness=3)
                    ## end for debug
                except ValueError:
                    pass
            header_width = corners_header[1][0] - corners_header[0][0]

            column_coords = [corners_header[0][0] + int(header_width * value) for value in header_columns]  # calculate size of each columm
            transaction_contents = []
            # process from transactions[0] to transactions[:-1]
            for transaction_index, transaction in enumerate(transactions[:-1]):
                content = [transaction.description, "", "", "", "", "", ntpath.basename(image_path.replace('.jpg', ''))]
                ymin = transactions[transaction_index].bounding_poly.vertices[2].y
                ymax = transactions[transaction_index + 1].bounding_poly.vertices[0].y
                for index in range(len(column_coords) - 1):
                    content_range = np.array(
                        [[column_coords[index], ymin], [column_coords[index + 1], ymin], [column_coords[index + 1], ymax], [column_coords[index], ymax]])
                    # cv2.polylines(rotated_image, [content_range], True, (0, 0, 255), 3)  # for debug
                    # cv2.imshow("image", rotated_image)  # for debug
                    # cv2.waitKey()  # for debug
                    for text in texts[1:]:
                        if istextboxinrange(content_range, text.bounding_poly.vertices):
                            content[index + 1] += text.description + " "  # todo: should optimize
                    transaction_contents.append(content)
                print(f"content: {content}")
                transaction_contents.append(content)

            # process last transaction: transactions[-1]
            content = [transactions[-1].description, "", "", "", "", "", ntpath.basename(image_path.replace('.jpg', ''))]
            ymin = transactions[-1].bounding_poly.vertices[2].y
            ymax = corners_footer[0][1]
            for index in range(len(column_coords) - 1):
                content_range = np.array(
                    [[column_coords[index], ymin], [column_coords[index + 1], ymin], [column_coords[index + 1], ymax], [column_coords[index], ymax]])
                # cv2.polylines(rotated_image, [content_range], True, (0, 0, 255), 3)  # for debug
                # cv2.imshow("image", rotated_image)  # for debug
                # cv2.waitKey()  # for debug
                for text in texts[1:]:
                    if istextboxinrange(content_range, text.bounding_poly.vertices):
                        content[index + 1] += text.description + " "  # todo: should optimize
            print(f"content: {content}")
            transaction_contents.append(content)
            # TODO: append step 8. post-processing before saving data here
            save_content(file_path=f"{sub_content_dir}/{ntpath.basename(image_path).replace('.jpg', '.csv')}", header=content_header,
                         contents=transaction_contents)  # step 7: save transaction to csv
            append_processed(log_processed_file, image_path)
