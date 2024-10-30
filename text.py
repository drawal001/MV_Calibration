from re import T
import numpy as np
import rm
import cv2

cam_cfg = rm.CameraConfig()
cam_cfg.grab_mode = rm.GrabMode.Continuous
cam_cfg.retrieve_mode = rm.RetrieveMode.SDK

cap = rm.MvCamera(cam_cfg)

while True:
    ret, frame = cap.read()
    if ret:
        img = frame.copy()
        cv2.imshow('img', img)

        key = cv2.waitKey(1)
        if key == 32:
            print(img.shape[:2])
        if key == 27:
            break

cv2.destroyAllWindows()

