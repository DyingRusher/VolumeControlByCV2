import cv2
import mediapipe as mp
import time 

mediaH = mp.solutions.hands
hands = mediaH.Hands()
mpDraw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)


ctime = 0
ptime = 0 


while True:
    success , img = cap.read()

    #converting to RGB
    img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #claculating fps and displaying it 
    ctime = time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime

    cv2.putText(img_rgb,str(int(fps)),(10,70),cv2.FONT_HERSHEY_DUPLEX,2,(255,255,255))

    #getting values os landmarks
    results = hands.process(img_rgb)
    if(results.multi_hand_landmarks):
        for H in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img_rgb,H,mediaH.HAND_CONNECTIONS)
            for id,lm in enumerate(H.landmark):
                #for dispaly in pixels 
                h, w ,c = img_rgb.shape
                cx ,cy = int(lm.x*w),int(lm.y*h)
                if id==4 or id==2:
                    cv2.circle(img_rgb,(cx,cy),10,(100,100,234),cv2.FILLED)
                print(id , cx,cy)

    cv2.imshow("Hey",img_rgb)
    # print(results.multi_hand_landmarks)

    
    # cv2.waitKey(2)
    interrupt = cv2.waitKey(1) 
    if interrupt & 0xFF == 27: # esc key
        break
