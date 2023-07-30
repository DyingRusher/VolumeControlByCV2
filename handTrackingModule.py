import cv2
import mediapipe as mp
import time 




class handTracker():
    def __init__(self,mode=False,maxHands = 2,detectionCon = 0.5,trackingCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon
        

        self.mediaH = mp.solutions.hands
        self.hands = self.mediaH.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    

    def findHands(self,img_rgb,draw=True):
        img_rgb = cv2.cvtColor(img_rgb,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        if draw:
            if (self.results.multi_hand_landmarks):
                for H in self.results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img_rgb,H,self.mediaH.HAND_CONNECTIONS)

        return img_rgb
    
    def findPosition(self,img_rgb,highlight = False,pointForHighlight = [],returnPoint=[]):
        posi =[]
        # results = self.hands.process(img_rgb)
        if(self.results.multi_hand_landmarks):
            for H in self.results.multi_hand_landmarks:
                for id,lm in enumerate(H.landmark):
                    #for dispaly in pixels 
                    h, w ,c = img_rgb.shape
                    cx ,cy = int(lm.x*w),int(lm.y*h)
                    if highlight:
                        for ids in pointForHighlight:
                            if id == ids:
                                posi.append([id,cx,cy])
                                cv2.circle(img_rgb,(cx,cy),10,(100,100,234),cv2.FILLED)
                    # print(id , cx,cy)
                    if not highlight:
                        posi.append([id,cx,cy])
        return posi
   
    # print(results.multi_hand_landmarks)

    
    # cv2.waitKey(2)
   




def main():


    
    cap = cv2.VideoCapture(0)

    
    ctime = 0
    ptime = 0 

    while True:
        success , img = cap.read()

        #converting to RGB
        img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        detector = handTracker()
        img_rgb = detector.findHands(img_rgb=img_rgb)
        pos = detector.findPosition(img_rgb,True,[3,6,18])
        print(pos)
        #claculating fps and displaying it 
        ctime = time.time()
        fps = 1/(ctime - ptime)
        ptime = ctime

        cv2.putText(img_rgb,str(int(fps)),(10,70),cv2.FONT_HERSHEY_DUPLEX,2,(255,255,255))
        cv2.imshow("Hey",img_rgb)

        interrupt = cv2.waitKey(1) 
        if interrupt & 0xFF == 27: # esc key
            break

if __name__ == "__main__":
    main()