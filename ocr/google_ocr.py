from .classes import *
import glob
import io
import os
import shutil
import time
from pathlib import Path
import cv2
import numpy as np
from google.cloud import vision
import json


def drawtextpoly(image, text, poly_color=(255, 0, 0), poly_thickness=1, show_label=False, text_color=(0, 255, 0),
                 text_thickness=1):
    poly = np.empty([4, 2], dtype=int)
    for i, point in enumerate(text.bounding_poly.vertices):
        poly[i] = [point.x, point.y]
    image = cv2.polylines(image, [poly], True, poly_color, poly_thickness)
    if show_label:
        # print("description", text.description)
        cv2.putText(image, text.description, poly[1], cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, text_thickness)


def fillpoly(image, poly):
    # poly = np.empty([4, 2], dtype=int)
    for iii, point in enumerate(text.bounding_poly.vertices):
        poly[iii] = [point.x, point.y]
    image = cv2.polylines(image, [poly], True, poly_color, poly_thickness)


def drawmask(mask, text):
    mask = cv2.circle(mask, (text.bounding_poly.vertices[1].x, text.bounding_poly.vertices[1].y), 1, (255, 255, 255),
                      -1)
    # polys = np.empty([4, 2], dtype=int)
    # for iii, point in enumerate(text.bounding_poly.vertices):
    #     polys[iii] = [point.x, point.y]
    # mask = cv2.fillPoly(mask, [polys], 255)


def isnumber(string):
    return string.replace('.', '').isdecimal()


def drawmask_money(mask, text):
    if isnumber(text.description):
        mask = cv2.circle(mask, (text.bounding_poly.vertices[1].x, text.bounding_poly.vertices[1].y), 5,
                          (255, 255, 255), -1)
    else:
        mask = cv2.circle(mask, (text.bounding_poly.vertices[1].x, text.bounding_poly.vertices[1].y), 180,
                          (0, 0, 0), -1)
    # polys = np.empty([4, 2], dtype=int)
    # for iii, point in enumerate(text.bounding_poly.vertices):
    #     polys[iii] = [point.x, point.y]
    # mask = cv2.fillPoly(mask, [polys], 255)


def googleocr(image_path, client, issort=True):
    # del result
    start_time = time.time()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    cvimage = vision.Image(content=content)
    # call api google ocr. return
    response = client.text_detection(image=cvimage)
    print("--- google excution time in %s seconds ---" % (time.time() - start_time))
    # start_time = time.time()
    # print("response.text_annotations", response.text_annotations)
    # save log
    # loggoogleocr(image_path, response)
    gocr_converter = list()
    for text in response.text_annotations:
        gocr_converter.append(TextOCR(text.description, 1.0, text.bounding_poly.vertices, None))
    # genrate data for trainning
    # ocrprocessing(image_path, response.text_annotations)
    if issort:
        return sort_textboxs(gocr_converter)
    else:
        return gocr_converter
