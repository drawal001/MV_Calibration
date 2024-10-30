import cv2
import numpy as np
import rm
from CalibrationConfig import *

data = np.load('/home/drawar/Desktop/CameraDemo/MV/calibration/param_save/calibration_param_0.02197450995774649.npz')
dist = data['dist_array']
mtx = data['mtx_array']

cam_cfg = rm.CameraConfig()
cam_cfg.grab_mode = rm.GrabMode.Continuous
cam_cfg.retrieve_mode = rm.RetrieveMode.OpenCV

cap = rm.MvCamera(cam_cfg)

cap.set(rm.CAMERA_MANUAL_EXPOSURE)
cap.set(rm.CAMERA_EXPOSURE, 5000)

cv2.waitKey(0)
while True:
    ret, frame = cap.read()
    if ret:
        h, w = frame.shape[:2]
        break

new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0, (w, h))
mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, new_camera_matrix, (w, h), 5)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

while True:
    ret, frame = cap.read()
    if ret:
        dst = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
        gray = dst.copy()
        cv2.line(dst, (0, int(h/2)), (w, int(h/2)), (0,0,255), 2)
        cv2.line(dst, (int(w/2), 0), (int(w/2), h), (0.0,255), 2)
        cv2.imshow('dst', dst)

        key = cv2.waitKey(1)
        if key == 32:
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            ret, centers = cv2.findCirclesGrid(gray, (calibration_size[1], calibration_size[0]), cv2.CALIB_CB_ASYMMETRIC_GRID)
            if ret:
                centers2 = cv2.cornerSubPix(gray, centers, (6, 6), (-1, -1), criteria)
                sum_ = []
                last_i = [0]
                count = 0
                for i in centers2:
                    count += 1
                    if count != 1 and (count - 1) % 7 != 0:
                        a_ = (last_i[0] - i[0]) ** 2
                        sum_.append(np.sqrt(a_))
                    last_i = i
                
                map_param = np.mean(sum_)
                map_param = center_distance / map_param  #单位 mm/像素
                print(f"map_param = {map_param}")

                # np.savez(map_param_save_path, map_param = map_param)
        if key == 27:
            break
    else:
        cv2.waitKey(0)

cv2.destroyAllWindows()
                
