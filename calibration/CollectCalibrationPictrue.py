import rm
import cv2
import os
from CalibrationConfig import save_path

cam_cfg = rm.CameraConfig()
cam_cfg.grab_mode = rm.GrabMode.Continuous
cam_cfg.retrieve_mode = rm.RetrieveMode.OpenCV

cap = rm.MvCamera(cam_cfg)

exposure = cap.get(rm.CAMERA_EXPOSURE)
print(f"old: {exposure}")

cap.set(rm.CAMERA_MANUAL_EXPOSURE)
cap.set(rm.CAMERA_EXPOSURE, 5000)

exposure = cap.get(rm.CAMERA_EXPOSURE)
print(f"new: {exposure}")

if not os.path.exists(save_path):
    os.makedirs(save_path)

num = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print('error')
        break
    else:
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        if key == 32:
            num += 1
            if(cv2.imwrite(save_path + f'{num}.jpg', frame)):
                print(f"save {num}.jpg")
            else:
                print(f"save {num}.jpg failed")
        if key == 27:
            break
    
# cap.release()
cv2.destroyAllWindows()
