import numpy as np
import cv2

class HSV():

    def __init__(self,img_url):

        global img
        self.url = img_url
        img = cv2.imread(self.url)

    def pick_color(event,x,y,flags,param):

        if event == cv2.EVENT_LBUTTONDBLCLK:
            global hsv
            bgr = img[y,x]
            hsv = cv2.cvtColor(np.uint8([[bgr]]),cv2.COLOR_BGR2HSV)

    def get_value(self,pick_color=pick_color):

        cv2.namedWindow('image')
        cv2.setMouseCallback('image',pick_color)

        while True:

            cv2.imshow('image',img)

            if cv2.waitKey(10) & 0xFF == ord('q'):

                break
            
        cv2.destroyAllWindows()

    def get_boundings(self,h=20,s=50,v=60):
        
        hue = int(hsv[0][0][0])
        sat = int(hsv[0][0][1])
        val = int(hsv[0][0][2])
        
        lower_bounding = np.array([hue-h,sat-s,val-v])
        upper_bounding = np.array([hue+h,sat+s,val+v])
        
        return lower_bounding,upper_bounding




if __name__ == '__main__':

    a = HSV('/home/user_name/roi.jpg')
    a.get_value()
    lower,upper = a.get_boundings()
    print(lower,upper)