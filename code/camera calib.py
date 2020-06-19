import numpy as np
import cv2
import glob


cap = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)
#cap.set(3,256)
#cap.set(4,192)
#cap2.set(3,256)
#cap2.set(4,192)

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpointsL = [] # 3d point in real world space
imgpointsL = [] # 2d points in image plane.
objpointsR = []
imgpointsR = []

check = 1
while (check < 12):
    ret1, img = cap.read()
    ret2, img2 = cap2.read()
    if ret1 == True & ret2 == True:
        print 'Image number', check , 'acquired'
        #images = glob.glob('*.jpg')

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        cv2.imshow ('Left',gray)
        cv2.imshow ('Right',gray2)
        cv2.waitKey(0)
        # Find the chess board corners
        ret3, corners = cv2.findChessboardCorners(gray, (9,6),None)
        ret4, corners2 = cv2.findChessboardCorners(gray2, (9,6),None)
        # If found, add object points, image points (after refining them)
        if ret3 == True & ret4 == True:
            print 'chessboard found'
            objpointsL.append(objp)
            objpointsR.append(objp)

            corners3 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            corners4 = cv2.cornerSubPix(gray2,corners2,(11,11),(-1,-1),criteria)
            imgpointsL.append(corners3)
            imgpointsR.append(corners4)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (9,6), corners,ret2)
            img2 = cv2.drawChessboardCorners(img2, (9,6), corners2, ret3)
            cv2.imshow('Left',img)
            cv2.imshow('Right', img2)
            cv2.waitKey(500)
            check = check + 1
        else:
            print 'chessboard not found'
        print 'Press anykey to aquire next image'
        cv2.waitKey(0)
    else:
        print 'Waiting for frame'
cv2.destroyAllWindows()
print 'Beginning Callibration, press any key to continue'
cv2.waitKey(0)
ret5, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpointsL, imgpointsL, gray.shape[::-1],None,None)
ret6, mtx2, dist2, rvecs2, tvecs2 = cv2.calibrateCamera(objpointsR, imgpointsR, gray.shape[::-1],None,None)
print 'mtx Left'
print mtx
print 'dist Left'
print dist
print 'rvecs Left'
print rvecs
print 'tvecs Left'
print tvecs
print 'mtx Right'
print mtx2
print 'dist Right'
print dist2
print 'rvecs Right'
print rvecs2
print 'tvecs Right'
print tvecs2

ret7, img = cap.read()
ret8, img2 = cap2.read()
gray3 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray4 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
h,  w = gray3.shape[:2]
h2,  w2 = gray4.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
newcameramtx2, roi2=cv2.getOptimalNewCameraMatrix(mtx2,dist2,(w2,h2),1,(w2,h2))
print 'newcameramtx Left'
print newcameramtx
print 'newcameramtx Right'
print newcameramtx2

# undistort
dst = cv2.undistort(gray3, mtx, dist, None, newcameramtx)

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
cv2.imwrite('calibresult.png',dst)
cv2.imshow('Callibration Result',dst)

#np.savetxt('mtx', mtx, delimiter = ',')
#np.savetxt('dist', dist, delimiter = ',')
#np.savetxt('rvecs', rvecs, delimiter = ',')
#np.savetxt('tvecs', tvecs, delimiter = ',')
#np.savetxt('ncm', newcameramtx, delimiter = ',')

#np.savetxt('mtx2', mtx2, delimiter = ',')
#np.savetxt('dist2', dist2, delimiter = ',')
#np.savetxt('rvecs2', rvecs2, delimiter = ',')
#np.savetxt('tvecs2', tvecs2, delimiter = ',')
#np.savetxt('ncm2', newcameramtx2, delimiter = ',')
# undistort
#dst = cv2.undistort(gray2, mtx, dist, None, newcameramtx)

# crop the image
#x,y,w,h = roi
#dst = dst[y:y+h, x:x+w]
#cv2.imwrite('calibresult.png',dst)
#cv2.imshow('Callibration Result',dst)
