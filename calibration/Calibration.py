import rm
import cv2
from CalibrationConfig import *
import numpy as np
import glob

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((calibration_size[1] * calibration_size[0], 3), np.float32)
objp[:,:2] = np.mgrid[0:calibration_size[1], 0:calibration_size[0]].T.reshape(-1, 2)

objpoints = []
imgpoints = []


images = glob.glob(save_path + "*.jpg")
for image in images:
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, centers = cv2.findCirclesGrid(gray, (calibration_size[1], calibration_size[0]), cv2.CALIB_CB_ASYMMETRIC_GRID)

    if ret:
        objpoints.append(objp)

        centers2 = cv2.cornerSubPix(gray, centers, (6, 6), (-1, -1), criteria)
        imgpoints.append(centers2)

        img = cv2.drawChessboardCorners(img, (calibration_size[1], calibration_size[0]), centers2, ret)
        cv2.imshow('img', img)
        key = cv2.waitKey(0)
        if key == 27:
            break
    else:
        print("Failed to find circle grid")

cv2.destroyAllWindows()


#标定
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    mean_error += error
total_error = mean_error / len(objpoints)

print(f"mean_error = {total_error}")

# np.savez(calibration_result_save_path + f"_{total_error}", dist_array=dist, mtx_array=mtx)