import cv2 as cv
import numpy as np
import time
    

class contour_finder():

    def __init__(self, frame):
        self.frame = frame

    #contourleri bulup bunları çıktı veren bir fonksiyon.
    def contour_calculator(self, frame):
            
        #her bir kareyi griye çevirdim, threshold uygulayabilmek için
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        #Gri resme threshold ve morfolojik işlemler uyguladım.
        _, threshold = cv.threshold(gray, 225, 255, cv.THRESH_BINARY)
        dilation_threshold = cv.dilate(threshold, (5,5), iterations=4)
        kernel = np.ones((5,5),np.uint8)
        erosion = cv.erode(dilation_threshold,kernel,iterations = 4)

        #İşlediğim görseldeki kontürleri buldum
        contours, _ = cv.findContours(
            erosion, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        return contours #kontürleri çıktı olarak verdim


class rectangle():

    def __init__(self, frame):
        self.frame = frame

    #dikdörtgen tespit algoritması.
    def rectangle_finder(self, frame):
        try:
            for contour in contour_finder.contour_calculator(frame):
            
                # nesne belirleme algoritması olan approxpolydp kullandım.
                approx = cv.approxPolyDP(
                    contour, 0.0175 * cv.arcLength(contour, True), True)

                # dikdörtgen tespiti yaptım
                if len(approx) == 4:
                    return True

                else:
                    return False

        except:#kontür bulamaması durumunda hata vermek yerine uyarı mesajı alacağız.
            print("Dikdörtgen kontürleri bulunamadı.")

    #dikdörtgen hareket algoritması
    def rectangle_move(self, frame):
        (cam_x, cam_y) = frame.shape[:2]#kameranın merkezini buldum.
        contours = contour_finder.contour_calculator(frame)#kontürleri buldum.

        for contour in contours: #kontürler arasında gezecek döngü oluşturdum.
            rotate_list = [0] * 4 #hareket işleminden sonra hareket komutu takılı kalmaması için sıfırladım.
            area = cv.contourArea(contour)#şekle yakınlığı anlayabilmek için alan hesabı yaptım.

            #Doğru şekli algılayabilmek için belirli bir alan sınırı koydum.
            while (area > 1000 and area < 10000):
                M = cv.moments(contour)
                if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                
                #dikdörtgenin kısa kenar uzunluğuna eriştim.
                d_x,d_y,d_w,d_h = cv.boundingRect(contour)
                if(abs(d_x - d_w) > abs(d_y - d_h)):
                    kisa_kenar = abs(d_y - d_h)
                elif(abs(d_x - d_w) < abs(d_y - d_h)):
                    kisa_kenar = abs(d_x - d_w)

                #diktörgenin ortasına şeklin o anki büyüklüğünün q katı kadar küçük yapay dikdörtgen oluşturdum.
                q = 3
                k = kisa_kenar/q #k = ufak dikdörtgenin kenarı
                a = (-1)*(kisa_kenar/(2*q))        
                
                #yakınlaşmak için hız katsayısı
                gain = 0.2
                #Merkezin içinde değilse hareket komutu verilecek.
                while(abs(cam_x - cx) > k/2):
                    #sanal küçük dikdörtgenin ortası ile kamera ortasının kıyaslanması. X ekseni için
                    if(cam_x - cx < k/2):
                        #yaklaştıkça hızın yavaşlaması.
                        rotate_list[0] = 50 + (gain * (cam_x - cx))
                        #hız limiti.
                        if (rotate_list[0] < 10):
                            rotate_list[0] = 10
                            return rotate_list
                            
                    elif (cam_x - cx > k/2):
                        rotate_list[0] = -50 +(gain * (cam_x - cx))
                        if (rotate_list[0] > -10):
                            rotate_list[0] = -10
                            return rotate_list
                        return rotate_list
                
                #üstteki karşılaştırmanın y ekseni için yapılmış hali.
                while(abs(cam_y - cy) > k/2):
                    if (cam_y - cy < k/2):
                        rotate_list[2] = 50 + (gain * (cam_x - cx))
                        if (rotate_list[2] < 10):
                            rotate_list[2] = 10
                            return rotate_list
                        return rotate_list

                    elif (cam_y - cy > k/2):
                        rotate_list[2] = -50 + (gain * (cam_x - cx))
                        if (rotate_list[2] > -10):
                            rotate_list[2] = -10
                            return rotate_list
                        return rotate_list
                
                #kamera ortalandıysa araç yavaş yavaş ilerlesin.
                rotate_list = [0, 15, 0, 0]
                print(rotate_list)
            
            #kontürleri bütün olarak göremeyeceğim kadar yakınlaştığında aracın düz gitmesini belirttim.
            if (area > 10000):
                rotate_list[1] = 50
                return rotate_list

class circle():
    
    def __init__(self, frame, contour):
        self.frame = frame
        self.contour = contour

    #daire bulma algoritması.
    def circle_finder(self, frame):
        contours = contour_finder.contour_calculator(frame)
        
        try:
            #kontürlerde gezebilmek için döngü oluşturdum.
            for contour in contours:

                # nesne belirleme algoritması olan approxpolydp kullandım.
                approx = cv.approxPolyDP(
                    contour, 0.0175 * cv.arcLength(contour, True), True)

                if len(approx) > 8: #daire ise True döndürecek koşul.
                    return True

                else:
                    return False
        except:#kontür bulamaması durumunda hata vermek yerine uyarı mesajı alacağız.
            print("Daire kontürleri bulunamadı.")
    
    #daireye hareket algoritması.
    def circle_move(self, frame, contour):
        (cam_x, cam_y) = frame.shape[:2] #kameranın merkezini buldum.        
        contours = contour_finder.contour_calculator(frame) #kontürleri buldum.

        for contour in contours: #kontürler arasında gezecek döngü oluşturdum.
            rotate_list = [0] * 4 #hareket işleminden sonra hareket komutu takılı kalmaması için sıfırladım.
            area = cv.contourArea(contour) 

            #ana şekli yüzde kaç oranında küçültüp merkeze çizeceğim yapay dairenin yarıçapı a. (değiştirilebilir.)
            a = 5
            R = (area / 3.14)**0.5
            r = ((R**2)/a)**0.5 
            r = int(r)

            #sadece ana şekle odaklanabilmek için alan filtreleme ve şekli isimlendirme
            while (area > 1000 and area < 10000):

                #merkeze daire çizme ve merkezi isimlendirme
                M = cv.moments(contour)
                if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])

                #yakınlaşmak için hız katsayısı
                gain = 0.2
                #Merkezin içinde değilse hareket komutu verilecek.
                while(abs(cam_x - cx) > r):
                    #sanal küçük dikdörtgenin ortası ile kamera ortasının kıyaslanması. X ekseni için
                    if(cam_x - cx < r):
                        #yakınlaştıkça hızı azalıyor.
                        rotate_list[0] = 50 + (gain * (cam_x - cx))
                        #hız limiti.
                        if (rotate_list[0] < 10):
                            rotate_list[0] = 10
                            return rotate_list
                        return rotate_list

                    elif (cam_x - cx > r):
                        rotate_list[0] = -50 +(gain * (cam_x - cx))
                        if (rotate_list[0] > -10):
                            rotate_list[0] = -10
                            return rotate_list
                        return rotate_list

                #üstteki karşılaştırmanın y ekseni için yapılmış hali.
                while(abs(cam_y - cy) > r):
                    if (cam_y - cy < r):#yukarı çık
                        rotate_list[2] = 50 + (gain * (cam_x - cx))
                        if (rotate_list[2] < 10):
                            rotate_list[2] = 10
                            return rotate_list
                        return rotate_list
                
                    elif (cam_y - cy > r):#aşağı in
                        rotate_list[2] = -50 + (gain * (cam_x - cx))
                        if (rotate_list[2] > -10):
                            rotate_list[2] = -10
                            return rotate_list
                        return rotate_list

                #kamera ortalandıysa araç yavaş yavaş ilerlesin.
                rotate_list = [0, 15, 0, 0]
                print(rotate_list)

            #kontürleri bütün olarak göremeyeceğim kadar yakınlaştığında aracın düz gitmesini belirttim.
            if (area > 10000):
                rotate_list[1] = 50
                return rotate_list