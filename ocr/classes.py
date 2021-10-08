from PIL import Image
import cv2
import imagehash
import numpy as np


class Vertice:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class BoundingPoly:
    def __init__(self, vertices):
        self.vertices = [Vertice(item.x, item.y) for item in vertices]


class TextOCR:
    def __init__(self, description, confidence_score, vertices, id):
        self.bounding_poly = BoundingPoly(vertices)
        self.description = description
        self.confidence_score = confidence_score
        self.id = id


def ocrprocessing(image_path, textboxs):
    textboxs = list(textboxs)
    image = cv2.imread(image_path)
    ocrlabel = open("/media/hungtooc/STORED DATA/source/private/documment_kyc/data/label.txt", "a", encoding='utf8')
    for textbox in textboxs[1:]:
        ys, xs = [vertice.y if vertice.y > 0 else 0 for vertice in textbox.bounding_poly.vertices], [
            vertice.x if vertice.x > 0 else 0 for vertice
            in
            textbox.bounding_poly.vertices]
        image_text = image[min(ys):max(ys), min(xs):max(xs)]
        # print(textbox.description, textbox.description)
        # print("image_text.shape", image_text.shape, textbox.description, textbox.bounding_poly.vertices, (xs, ys))
        if min(image_text.shape) == 0:
            continue
        img = cv2.cvtColor(image_text, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        image_name = str(imagehash.average_hash(im_pil)) + ".jpg"
        # print(image_name)
        cv2.imwrite("/media/hungtooc/STORED DATA/source/private/documment_kyc/data/images/" + image_name, image_text)
        ocrlabel.write(image_name + " " + textbox.description + "\n")
    ocrlabel.close()


def sort_textboxs(textboxs):
    """
sắp xếp polys từ trên xuống dưới và từ trái sang phải theo đúng qui cách viết chữ VN
    :param textboxs:
    """
    textboxs = list(textboxs)
    for i in range(1, len(textboxs) - 1):
        for ii in range(i + 2, len(textboxs)):
            if textboxs[i].bounding_poly.vertices[0].x > textboxs[ii].bounding_poly.vertices[0].x:
                textboxs[i], textboxs[ii] = textboxs[ii], textboxs[i]
    return textboxs


def detect_line(mask):
    imgLines = cv2.HoughLinesP(mask, 10, np.pi / 90, 70, minLineLength=2000, maxLineGap=10000)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    if imgLines is not None:
        for i in range(len(imgLines)):
            for x1, y1, x2, y2 in imgLines[i]:
                cv2.line(mask, (x1, y1), (x2, y2), (255, 255, 255), 2)
    return mask
