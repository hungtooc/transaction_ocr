import cv2
import cv2 as cv
import numpy as np


def filter_matches(kp1, kp2, matches, ratio=0.75):
    mkp1, mkp2 = [], []
    for m in matches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            m = m[0]
            mkp1.append(kp1[m.queryIdx])
            mkp2.append(kp2[m.trainIdx])
    p1 = np.float32([kp.pt for kp in mkp1])
    p2 = np.float32([kp.pt for kp in mkp2])
    kp_pairs = zip(mkp1, mkp2)
    return p1, p2, list(kp_pairs)


def ObjectMatching(image: object, template, detector):
    """

        :param image: checked image
        :param template: check image
        :param detector: default sift
        :return:
        """
    stock_image = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    objects = []
    FLANN_BASED_MATCHER = 1
    index_params = dict(algorithm=FLANN_BASED_MATCHER, trees=30)
    # flann_params = dict(algorithm=FLANN_INDEX_LSH,
    # table_number=6,  # 12
    # key_size=12,  # 20
    # multi_probe_level=1)
    search_params = dict(checks=20)
    # Create flann matcher
    matcher = cv2.FlannBasedMatcher(index_params, search_params)
    kpts2, descs2 = detector.detectAndCompute(image, None)
    kpts1, descs1 = detector.detectAndCompute(template, None)
    # knnMatch to get Top2
    matches = matcher.knnMatch(descs1, descs2, 2)
    # appended code
    p1, p2, kp_pairs = filter_matches(kpts1, kpts2, matches)
    if len(p1) >= 4:
        H, status = cv.findHomography(p1, p2, cv.RANSAC, 5.0)
        print('%d / %d  inliers/matched' % (np.sum(status), len(status)))
    else:
        H, status = None, None
        print('%d matches found, not enough for homography estimation' % len(p1))
    h1, w1 = template.shape[:2]
    h2, w2 = image.shape[:2]
    if H is not None:
        corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
        corners = np.int32(cv.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2))
        return kpts2, corners
    else:
        return
