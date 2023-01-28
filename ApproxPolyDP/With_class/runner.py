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
            pass


        
        
"""        
#daire şekli için:
            else:
                area = cv.contourArea(contour)
                
                #ana şekli yüzde kaç oranında küçültüp merkeze çizeceğim yapay dairenin yarıçapı a. (değiştirilebilir.)
                a = 5
                R = (area / 3.14)**0.5
                r = ((R**2)/a)**0.5 
                r = int(r)

                #sadece ana şekli bulmak için alan filtreleme ve şekli isimlendirme
                if (area > 1000 and area < 10000):
                    cv.drawContours(frame, [contour], 0, (255, 0, 0), -1)
                    cv.putText(frame, 'Y', (contour[0][0][0], contour[0][0][1]), cv.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)

                    #merkeze daire çizme ve merkezi isimlendirme
                    M = cv.moments(contour)
                    if M['m00'] != 0:
                        Cx = int(M['m10']/M['m00'])
                        Cy = int(M['m01']/M['m00'])
                        cv.drawContours(frame, [contour], -1, (0, 255, 0), 2)
                        cv.circle(frame, (cx, cy), r, (0, 0, 255), 3) #içi boş ve daire boyutuyla orantılı bir çember çizdir.
                        M_2 = cv.moments(contour)#bu kısımdan emin değilim küçük dairenin merkez koordinatlarına ulaşmaya çalıştım.
                        if M_2['m00'] != 0:
                            cx = int(M['m10']/M['m00'])
                            cy = int(M['m01']/M['m00'])
                             
                        cv.putText(frame, "center", (cx - 20, cy - 20),
	                			cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)


                    while (area < 10000): #şekle aşırı yakın olmadığında şekli ortalamak için döngü
                        if(cam_x - cx < r):
                            x = 127
                            y = 0
                            z = 0
                        if (cam_x - cx > r):
                            x = -127
                            y = 0
                            z = 0 

                        if (cam_y - cy < r):
                            x = 0
                            y = 127
                            z = 0
                        if (cam_y - cy > r):
                            x = 0
                            y = -127
                            z = 0
                    
                    #kontürleri bütün olarak göremeyeceğim kadar yakınlaştığında düz gitmesini belirttim.
                    if (area > 10000):
                        x = 0
                        y = 0
                        z = 127
                        cv.waitKey(7)


                print(f"x: {cx} y: {cy}")

        # kontürleri çizdikten sonra görüntülemek
        cv.imshow('shapes', frame)

        cv.waitKey(1)
        #cv2.destroyAllWindows()"""