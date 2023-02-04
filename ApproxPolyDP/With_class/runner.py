import cv2 as cv
import numpy as np
import classes as shape_detector
import time

#aynı şekilden tekrar geçmemek için koydum.
rectangle_pass = False
small_circle_pass = False
big_circle_pass = False

#Videoyu okudum.
cap = cv.VideoCapture('camera.mp4')

while (cap.isOpened()):

    ret, frame = cap.read()
    if ret == True:
        
        
        if ((rectangle_pass == False) and (shape_detector.rectangle.rectangle_finder(frame) == True)):
            rectangle_rotate_list = shape_detector.rectangle.rectangle_move(frame)
            
            if (rectangle_rotate_list == [0, 50, 0, 0]):#eğer şekil geçebilecek yakınlıktaysa 7 saniye ileri gitsin ve dikdörtgen arama döngüsü kırılsın.
                print(rectangle_rotate_list)
                time.sleep(7)
                rectangle_pass = True
                
                #180 derece dönme 
                rectangle_rotate_list = [0, 0, 0, 20]
                time.sleep(4)
                print(rectangle_rotate_list)
                break

            print(rectangle_rotate_list)
        

        #Daire için hareket çıktı listesi oluşturuyorum.
        elif((small_circle_pass == False) and (shape_detector.circle.circle_finder(frame) == True)):
            contours = shape_detector.contour_finder.contour_calculator(frame)
            sorted_contours = sorted(contours, key=cv.contourArea, reverse=False) #birden fazla daire algılaması halinde küçükten büyüğe sıraladım.
            small_circle = sorted_contours[0]#en küçük daire.

            small_circle_rotate_list = shape_detector.circle.circle_move(frame, small_circle)
            
            if (small_circle_rotate_list == [0, 50, 0, 0]):
                print(small_circle_rotate_list)
                time.sleep(7)
                small_circle_pass = True

                #180 derece dönme
                small_circle_rotate_list = [0, 0, 0, 20]
                print(small_circle_rotate_list)
                time.sleep(4)
                break

            print(small_circle_rotate_list)

        elif((big_circle_pass == False) and (shape_detector.circle.circle_finder(frame) == True)):
            
            contours = shape_detector.contour_finder.contour_calculator(frame)
            sorted_contours = sorted(contours, key=cv.contourArea, reverse=True) #birden fazla daire algılaması halinde büyükten küçüğe sıraladım.
            big_circle = sorted_contours[0]#büyük daire.

            big_circle_rotate_list = shape_detector.circle.circle_move(frame, big_circle)
            
            if (big_circle_rotate_list == [0, 50, 0, 0]):
                print(big_circle_rotate_list)
                time.sleep(7)
                big_circle_pass = True

                #180 derece dönme
                big_circle_rotate_list = [0, 0, 0, 20]
                print(big_circle_rotate_list)
                time.sleep(4)
                break

            print(big_circle_rotate_list)
        
        else:
            rotate_list = [0] * 4
            print (rotate_list)