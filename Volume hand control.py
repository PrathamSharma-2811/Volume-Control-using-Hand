import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)  # Checks for camera

mpHands = mp.solutions.hands  # identify or detect hand or finger
hands = mpHands.Hands()  # complete the initialization configuration of hands
mpDraw = mp.solutions.drawing_utils

# To access speaker through the library pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volbar = 400  # its the volume bar that i have declared
volper = 0  # its volume percentage that i have declared

volMin, volMax = volume.GetVolumeRange()[:2]
# the maximum and minimum range can be discovered by these to variables
while True:
    success, img = cap.read()  # value is =1 then it means condition is true and camera will execute and vice-versa
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # we Convert the capture image to rgb
    # COLOR_BGR2RGB this function convert the captured image to RGB ie. red,green,blue
    # here rgb reffers to a system that  represens the colors to be used on a computer
    # Collection of gesture information
    results1 = hands.process(imgRGB)  # completes the image processing.

    llmList = []  # empty list
    if results1.multi_hand_landmarks:  # list of all hands detected.
        # accessing the list, we will get the info of each hand's corresponding flag bit
        for handlandmark in results1.multi_hand_landmarks:
            for id, lm2 in enumerate(handlandmark.landmark):  # adding counter and returning it
                # enumerate function convert the collected data into enumerate object

                # Get finger joint points
                h, w, _ = img.shape  # this h and w provides the height and width of image
                cx, cy = int(lm2.x * w), int(lm2.y * h)  # these cx and cy gives the center points
                llmList.append([id, cx, cy])  # adding to the empty list llmList
            mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)
    # here LLM stands for landmarks
    if llmList != []:
        # we get  the value at a point
        # x      #y
        x1, y1 = llmList[4][1], llmList[4][2]  # thumb representer
        x2, y2 = llmList[8][1], llmList[8][2]  ##index finger representer
        # creating circle at the tips of thumb and index finger
        cv2.circle(img, (x1, y1), 13, (255, 0, 0), cv2.FILLED)  # image #fingers #radius #rgb
        cv2.circle(img, (x2, y2), 13, (255, 0, 0), cv2.FILLED)  # image #fingers #radius #rgb
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)  # create a line b/w tips of index finger and thumb

        length = hypot(x2 - x1, y2 - y1)
        # using numpy we  will find our length,by convertingthe  hand range in terms of volume range which is  -63.5 to 0
        vol = np.interp(length, [30, 350], [volMin, volMax])
        volbar = np.interp(length, [30, 350], [400, 150])
        volper = np.interp(length, [30, 350], [0, 100])

        print(vol, int(length))
        volume.SetMasterVolumeLevel(vol, None)

        # Hand range 30 - 350
        # Volume range -63.5 - 0.0
        # creating volume bar for volume level
        cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255),
                      4)  # vid ,initial position ,ending position ,rgb ,thickness
        cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, f"{int(volper)}%", (10, 40), cv2.FONT_ITALIC, 1, (0, 255, 98), 3)
        # display the information of  volume percentage ,location,font of text,length,rgb color,thickness
    cv2.imshow('Image', img)  # Show the video
    if cv2.waitKey(1) & 0xff == ord(' '):  # By using spacebar delay will stop
        break

cap.release()  # we will stop the camera      
cv2.destroyAllWindows()  # All windows will be terminated

print('code executed Pratham')