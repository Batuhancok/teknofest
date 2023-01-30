import cv2 as cv
import numpy as np
import classes as shape_detector

#sadece 3 şekilden geçmesi için koydum.
shape_counter = 0

#Videoyu okudum.
cap = cv.VideoCapture('Shapes Song.mp4')

while (cap.isOpened()):

    ret, frame = cap.read()
    if ret == True:
        
        #dikdörtgen için hareket output listesi oluşturuyorum.
        rectangle_rotate_list = shape_detector.rectangle.rectangle_finder(frame)

        #sadece dikdörtgen için bir geçiş döngüsü.
        while (shape_counter == 0):

            if (rectangle_rotate_list == [0, 0, 100, 0]):#eğer şekil geçebilecek yakınlıktaysa 7 saniye ileri gitsin ve dikdörtgen arama döngüsü kırılsın.
                print(rectangle_rotate_list)
                cv.waitKey(7)
                shape_counter = 1
                break

            print(rectangle_rotate_list)
        
        #dikdörtgen için hareket output listesi oluşturuyorum.
        circle_rotate_list = shape_detector.circle.circle_finder(frame)

        #ilk şekilden (dikdörtgen) geçerse araç, küçük daireyi aramaya başlayacak.
        while (shape_counter == 1):
            contours = shape_detector.contour_finder.contour_calculator(frame)
            
            while (shape_detector.circle.circle_finder(frame) == True):
                sorted_contours = sorted(contours, key=cv.contourArea, reverse=True) #büyükten küçüğe kontürleri sıraladım.
                small_circle = sorted_contours[1]

                small_circle_rotate_list = shape_detector.circle.circle_move(frame, small_circle)
                small_circle_rotate_list
                
                if (small_circle_rotate_list == [0, 0, 100, 0]):
                    print(small_circle_rotate_list)
                    cv.waitKey(7)
                    shape_counter = 2
                    break
                
                print(small_circle_rotate_list)


        
        while (shape_counter == 2):
            contours = shape_detector.contour_finder.contour_calculator(frame)

            while (shape_detector.circle.circle_finder(frame) == True):
                sorted_contours = sorted(contours, key=cv.contourArea, reverse=True) #büyükten küçüğe kontürleri sıraladım.
                big_circle = sorted_contours[0]

                big_circle_rotate_list = shape_detector.circle.circle_move(frame, big_circle)
                big_circle_rotate_list

                if (big_circle_rotate_list == [0, 0, 100, 0]):
                    print(big_circle_rotate_list)
                    cv.waitKey(7)
                    shape_counter = 3
                    break
                
                print(big_circle_rotate_list)