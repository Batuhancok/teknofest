import cv2 as cv
import imutils
import numpy as np

img = cv.imread('case1.png')
shapes = list()


class shape_detector:
    def __init__(self, img):
        self.img = img

    def rectangle_detector(self):
        img = self.img
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

        #merkezi belirlemeyi ekle
        shapes.append(img)

    def circle_detector(self):
        img = self.img
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img = cv.medianBlur(img, 5)
        cimg = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
        circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 20,
                                  param1=20, param2=80, minRadius=0, maxRadius=100)

        circles = np.uint16(np.around(circles))

        for i in circles[0, :]:
            # draw the outer circle
            cv.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

        hsv = cv.cvtColor(cimg, cv.COLOR_BGR2HSV)
        lower_blue = np.array([36, 50, 70])
        upper_blue = np.array([89, 255, 255])
        mask = cv.inRange(hsv, lower_blue, upper_blue)

        cv.imshow('circle', cimg)
        cv.waitKey(0)
        #cv.destroyAllWindows()

        contours, hierarchy = cv.findContours(mask, 1, 2)
        for i in contours:
            #cnt = contours[i]
            area = cv.contourArea(i)
            print(area)

shape_detector(img).circle_detector()
shape_detector(img).rectangle_detector()