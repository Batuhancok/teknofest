import cv2 as cv
import imutils
import numpy as np

img = cv.imread('case1.png')
img_2 = cv.imread('case1.png', 0)
shapes = list()

class rectangle_detector(img):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    thresh_img = cv.threshold(gray_img, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

    cnts = cv.findContours(thresh_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for cnt in cnts:
        x1, y1 = cnt[0][0]
        approx = cv.approxPolyDP(cnt, 0.01 * cv.arcLength(cnt, True), True)
        if len(approx) == 4:
            x, y, w, h = cv.boundingRect(cnt)
            ratio = float(w) / h
            if ratio >= 0.9 and ratio <= 1.1:
                cv.putText(img, 'Rectangle', (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                img = cv.drawContours(img, [cnt], -1, (0, 255, 0), 3)
            else:
                cv.putText(img, 'Rectangle', (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                img = cv.drawContours(img, [cnt], -1, (0, 255, 0), 3)
    cv.imshow('Image',img)
    cv.waitKey(0)
    shapes.append(img)

class circle_detector(img):
    img_2 = cv.medianBlur(img_2, 5)
    cimg = cv.cvtColor(img_2, cv.COLOR_GRAY2BGR)
    circles = cv.HoughCircles(img_2, cv.HOUGH_GRADIENT, 1, 20,
                              param1=20, param2=80, minRadius=0, maxRadius=100)

    circles = np.uint16(np.around(circles))

    for i in circles[0, :]:
        # draw the outer circle
        cv.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

    cv.imshow('detected circles', cimg)
    cv.waitKey(0)
    cv.destroyAllWindows()

    hsv = cv.cvtColor(cimg, cv.COLOR_BGR2HSV)
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])

    mask = cv.inRange(hsv, lower_blue, upper_blue)
    res = cv.bitwise_and(cimg, cimg, mask=mask)

    image, cnts, hierarchy = cv.findContours(res, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    cnt = sorted(cnts, key=cv.contourArea, reverse=True)
    #cnt[1] = ['Küçük Daire']
    shapes.append(cnt[1])
    cnt[0] = ['Büyük Daire']
    #shapes.append(cnt[0])"""


#bitwise_or işlemi ile iki resmi birleştir.
#öncelik sıralaması yap