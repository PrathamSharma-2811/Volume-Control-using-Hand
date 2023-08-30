import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

"""volume.GetMute()
volume.GetMasterVolumeLevel()

"""

# 1ST TO GET HAND
# TO GET LANDMARK OF HANDS


cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
lmdraw = mp.solutions.drawing_utils  # for landmark visualizationj in the image

while True:
    success, img = cap.read()
    colorimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(colorimg)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for morehandslm in results.multi_hand_landmarks:  # if more than 1 hand hand is found
            landmklist = []  # holds landmark of pixel value
            for id, lm in enumerate(morehandslm.landmark):
                # print(id,lm)                                # we need landmark 4 and 8 as of now landmark "4 for thumb and landmark 8 is for index finger"
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)  # converting landmarks to pixel value----------
                # print(id,cx,cy)
                landmklist.append([id, cx, cy])
                # print(landmklist)

        lmdraw.draw_landmarks(img, morehandslm,
                              mp_hands.HAND_CONNECTIONS)  # showing landmark in image and connecting them

        if landmklist:  # making circle at finger and thumb
            x1, y1 = landmklist[4][1], landmklist[4][2]
            x2, y2 = landmklist[8][1], landmklist[8][2]

            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (0, 255, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (25, 8, 7), 2)

            length = math.hypot(x2 - x1, y2 - y1)
            # print(length)

            # lenght < 50 neglect and lenght >250 neglect
            if length < 50:
                z1 = (x1 + x2) // 2
                z2 = (y1 + y2) // 2
                cv2.circle(img, (z1, z2), 10, (0, 255, 0), cv2.FILLED)

        rangofvol = volume.GetVolumeRange()
        minvol = rangofvol[0]
        maxvol = rangofvol[1]
        vol = np.interp(length, [50, 250], ([minvol, maxvol]))
        volbar = np.interp(length, [50, 250], (400, 150))
        volper = np.interp(length, [50, 250], [0, 100])
        print("Realtime volume percentage", volper)

        volume.SetMasterVolumeLevel(vol, None)
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 4)
        cv2.rectangle(img, (50, int(volbar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, str(int(volper)), (0, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 2)

    cv2.imshow("VOLUME CONTROL SYSTEM", img)
    cv2.waitKey(1)



