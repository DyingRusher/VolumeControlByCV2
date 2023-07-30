import cv2
import time
import numpy as np
import math
import handTrackingModule as htm
from ctypes import cast , POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
vol = cast(interface,POINTER(IAudioEndpointVolume))



wCam , hCam = 1230,2340
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0

minVol ,maxVol,a = vol.GetVolumeRange()
# vol.SetMasterVolumeLevel(-80,None)
detctor = htm.handTracker()
while True:
    success ,img = cap.read()
    img = detctor.findHands(img)
    posi = detctor.findPosition(img,True,[4,8],[4,8])   

    #for line
    if len(posi)!=0:
        x1,y1 = posi[0][1],posi[0][2]
        x2,y2 = posi[1][1],posi[1][2]
        cv2.line(img,(x1,y1),(x2,y2),(25,83,109),3)
        #for mid circle
        cx,cy = (x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(cx,cy),13,(230,231,4),cv2.FILLED)
        #calculating length
        lent = math.hypot(x2-x1,y2-y1)
        if lent<50:
            cv2.circle(img,(cx,cy),13,(8,3,234),cv2.FILLED)



        #calculating range and changing volume 
        volR = np.interp(lent,[0,200],[-65,0])
        print(lent,volR)
        vol.SetMasterVolumeLevel(volR,None)


    # print(posi)


    
    #fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime


    cv2.putText(img,f'FPS {str(int(fps))}',(20,30),cv2.FONT_ITALIC,1,(23,54,245),1)
    
    cv2.imshow("sd",img)

    
    
       
    

    interrupt = cv2.waitKey(1)
    if interrupt & 0xFF == 27:
        break
