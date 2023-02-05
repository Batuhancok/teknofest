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
        
        #dikdörtgenden geçmediyse ve onu bulduysa içinden geçsin.
        if ((rectangle_pass == False) and (shape_detector.rectangle.rectangle_finder(frame) == True)):
            
            #dikdörtgen için bir hareket listesi oluşturan komut.
            rectangle_rotate_list = shape_detector.rectangle.rectangle_move(frame)
            
            if (rectangle_rotate_list == [0, 50, 0, 0]):#eğer şekil geçebilecek yakınlıktaysa 7 saniye ileri gitsin ve dikdörtgen aaramyı bıraksın.
                print(rectangle_rotate_list)
                time.sleep(7)
                rectangle_pass = True
                
                #180 derece dönme 
                rectangle_rotate_list = [0, 0, 0, 20]
                print(rectangle_rotate_list)
                time.sleep(4)

                #döndükten sonra durma
                rectangle_rotate_list = [0] * 4
                print(rectangle_rotate_list)

            print(rectangle_rotate_list)
        

        #Küçük daireyi bulduysa ve onun içinden geçmediyse ona yönelsin.
        elif((small_circle_pass == False) and (shape_detector.circle.circle_finder(frame) == True)):
            contours = shape_detector.contour_finder.contour_calculator(frame)
            sorted_contours = sorted(contours, key=cv.contourArea, reverse=False) #birden fazla daire algılaması halinde küçükten büyüğe sıraladım.
            small_circle = sorted_contours[0]#en küçük daire.

            #küçük daire için bir hareket listesi oluşturan komut.
            small_circle_rotate_list = shape_detector.circle.circle_move(frame, small_circle)
            
            #geçecek kadar yakın komutu alıyorsak 7 saniye tüm komutları bırakıp ileri gitmeyi sürdürmeli.
            if (small_circle_rotate_list == [0, 50, 0, 0]):
                print(small_circle_rotate_list)
                time.sleep(7)
                small_circle_pass = True

                #180 derece dönsün.
                small_circle_rotate_list = [0, 0, 0, 20]
                print(small_circle_rotate_list)
                time.sleep(4)

                #döndükten sonra durma.
                small_circle_rotate_list = [0] * 4
                print(small_circle_rotate_list)

            print(small_circle_rotate_list)

        #büyük daireden geçmediyse ve onu bulduysa ona yönelsin.
        elif((big_circle_pass == False) and (shape_detector.circle.circle_finder(frame) == True)):
            
            contours = shape_detector.contour_finder.contour_calculator(frame)
            sorted_contours = sorted(contours, key=cv.contourArea, reverse=True) #birden fazla daire algılaması halinde büyükten küçüğe sıraladım.
            big_circle = sorted_contours[0]#büyük daire.

            #büyük daire için bir hareket listesi oluşturan komut.
            big_circle_rotate_list = shape_detector.circle.circle_move(frame, big_circle)
            
            #şekle çok yakında tüm komutları bırakıp 7 saniye ilerlesin.
            if (big_circle_rotate_list == [0, 50, 0, 0]):
                print(big_circle_rotate_list)
                time.sleep(7)
                big_circle_pass = True

                #180 derece dönme
                big_circle_rotate_list = [0, 0, 0, 20]
                print(big_circle_rotate_list)
                time.sleep(4)

                #döndükten sonra durma.
                big_circle_rotate_list = [0] * 4
                print(big_circle_rotate_list)

            print(big_circle_rotate_list)
        
        #tüm şekillerden geçtiyse dursun. Ama araç şekil algılayamasa da duruyor?
        else:
            rotate_list = [0] * 4
            print (rotate_list)