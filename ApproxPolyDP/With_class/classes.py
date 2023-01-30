import cv2 as cv
import numpy as np


class contour_finder():

    def __init__(self, frame):
        self.frame = frame

    def contour_calculator(self, frame):
        (cam_x, cam_y) = frame.shape[:2]
        cv.circle(frame, (cam_y // 2, cam_x // 2), 7, (255, 255, 255), -1)
            
        #her bir kareyi griye çevirdim, threshold uygulayabilmek için
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        #Gri resme threshold ve morfolojik işlemler uyguladım.
        _, threshold = cv.threshold(gray, 225, 255, cv.THRESH_BINARY)
        dilation_threshold = cv.dilate(threshold, (5,5), iterations=4)
        kernel = np.ones((5,5),np.uint8)
        erosion = cv.erode(dilation_threshold,kernel,iterations = 4)

        cv.imshow('thresh', threshold)
        cv.waitKey(1)

        #İşlediğim görseldeki kontürleri buldum
        contours, _ = cv.findContours(
            erosion, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
        return contours


class rectangle():

    def __init__(self, frame):
        self.frame = frame

    def rectangle_finder(self, frame):

        #kontürler arasında tek tek dolaşabildiğim döngü oluşturdum
        for contour in contour_finder.contour_calculator(frame):
            
            # nesne belirleme algoritması olan approxpolydp kullandım.
            approx = cv.approxPolyDP(
                contour, 0.0175 * cv.arcLength(contour, True), True)

            # dikdörtgen tespiti yaptım
            if len(approx) == 4:
                cv.drawContours(frame, [contour], 0, (0, 255, 255), -1)
                area = cv.contourArea(contour)

                #sadece ana şekli algılayabilmek için belirli bir alan sınırı koydum.
                if (area > 1000 and area < 10000):
                    cv.drawContours(frame, [contour], 0, (255, 0, 0), -1)
                    cv.putText(frame, 'D', (contour[0][0][0], contour[0][0][1]), cv.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)

                #şeklin ortasını buldum ve isimlendirdim.
                M = cv.moments(contour)
                if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    cv.drawContours(frame, [contour], -1, (0, 255, 0), 2)
                    
                    #diktörgen şeklin ortasına şeklin o anki büyüklüğünün q katı kadar küçük yapay dikdörtgen çizdirdim.
                    kisa_kenar = 0 #kısa kenarı bul.?????
                    q = 3
                    k = kisa_kenar/q
                    a = (-1)*(kisa_kenar/(2*q))
                    cv.rectangle(frame, (cx + a, cy - a), (cx - a, cy + a), (0, 0, 255), 3)
                    cv.putText(frame, "center", (cx - 20, cy - 20),
	        			cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                
                (cam_x, cam_y) = frame.shape[:2]#kameranın merkezini buldum.
                while (area < 10000): #şekle aşırı yakın olmadığında şekli ortalamak için döngü. k = ufak dikdörtgenin bir kenarı
                    rotate_list = [0] * 4

                    if(cam_x - cx < k/2):
                        rotate_list[0] = 100
                        return rotate_list

                    if (cam_x - cx > k/2):
                        rotate_list[0] = -100
                        return rotate_list

                    if (cam_y - cy < k/2):
                        rotate_list[1] = 100
                        return rotate_list
                        
                    if (cam_y - cy > k/2):
                        rotate_list[1] = -100
                        return rotate_list

                
                #kontürleri bütün olarak göremeyeceğim kadar yakınlaştığında aracın 7 saniye düz gitmesini belirttim.
                if (area > 10000):
                    rotate_list = [0] * 4
                    rotate_list[2] = 100
                    return rotate_list

class circle():
    
    def __init__(self, frame, contour):
        self.frame = frame
        self.contour = contour

    def circle_finder(self, frame):
        
        contours = contour_finder.contour_calculator(frame)

        #kontürlerde gezebilmek için döngü oluşturdum.
        for contour in contours:

            # nesne belirleme algoritması olan approxpolydp kullandım.
            approx = cv.approxPolyDP(
                contour, 0.0175 * cv.arcLength(contour, True), True)

            if len(approx) > 8: #daire ise True döndürecek koşul.
                return True
            
            else:
                return False
                
    
    def circle_move(self, frame, contour):
        
        contours = contour_finder.contour_calculator(frame)

        for contour in contours:
            area = circle.circle_finder(frame) #classın içindeki fonksiyonlar iç içe geçmiş şekilde çalışır mı?????

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
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    cv.drawContours(frame, [contour], -1, (0, 255, 0), 2)
                    cv.circle(frame, (cx, cy), r, (0, 0, 255), 3) #içi boş ve daire boyutuyla orantılı bir çember çizdirdim     
                    cv.putText(frame, "center", (cx - 20, cy - 20),
	            			cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                (cam_x, cam_y) = frame.shape[:2]

                while (area < 10000): #şekle aşırı yakın olmadığında şekli ortalamak için döngü
                    rotate_list = [0] * 4
                    
                    if(cam_x - cx < r):
                        rotate_list[0] = 100
                        return rotate_list

                    if (cam_x - cx > r):
                        rotate_list[0] = -100
                        return rotate_list
                    
                    if (cam_y - cy < r):
                        rotate_list[1] = 100
                        return rotate_list
                    
                    if (cam_y - cy > r):
                        rotate_list[1] = -100
                        return rotate_list

            #kontürleri bütün olarak göremeyeceğim kadar yakınlaştığında düz gitmesini belirttim.
            elif (area > 10000):
                rotate_list = [0] * 4
                rotate_list[2] = 100
                return rotate_list