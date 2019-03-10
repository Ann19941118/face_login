import cv2
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib

#TODO
#眨眼阈值(默认的阈值为3.0，或者为倒数1/3)

def eye_aspect_ratio(eye):
    #compute the distances between the twosets
    #计算垂直眼睛的距离
    #vertical eye landmarks(x,y)-cordinateion
    A = dist.euclidean(eye[1],eye[5])
    B = dist.euclidean(eye[2],eye[4])

    C = dist.euclidean(eye[0],eye[3])

    ear = (A+B)/(2.0*C)

    return ear

#construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p","--shape-predictor",required=True,
                help="path to facial landmark predictor")
ap.add_argument("-v","--video",type=str,default="",
                help = "path to input video file")
args = vars(ap.parse_args())

#define two constants, one for the eye aspect ratio to indicate
#blink and then a second constant for the number of consecutive
#this is important for project, and we can redefine them
eye_AR_thresh = 0.3
eye_AR_consec_frame = 3
#initialize the frame counters
counter = 0
total = 0

#初始化dlib的人脸检测器和面部标志检测器：
#initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

#grab the index of the facial landmarks for the left and right eye, respectively
(lStart,lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left-eye"]
(rstart,rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right-eye"]

#start the video stream thread
print("[INFO starting video stream thread...")
vc = FileVideoStream(args["video"]).start()
fileStream = True
#vs = VideoStream(src=0).start()
vs = VideoStream(usePiCamera=True).start()
time.sleep(1.0)

#loop over frames from the video stream
while True:

    if fileStream and not vs.more():
        break
    frame  = vs.read()
    frame = imutils.resize(frame,width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BAYER_BG2BGRA)

    rects = detector(gray,0)

    #loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then convert the facial
        # landmark(x,y)-coordinates to a Numpy
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        # extract the left and right eye coordinates, then use the
        # coordinates to copute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rstart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        ear = (leftEAR+rightEAR)/2.0

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame,[leftEyeHull],-1, (0,255,0),1)
        cv2.drawContours(frame,[rightEyeHull],-1,(0,255,0),1)

        #ckeck to see if the eye aspect ratio is below the blink
        #threshold, and if so, increment the blink frame counter
        if  ear<eye_AR_thresh:
            counter += 1
        #otherwise, the eye aspect ratio is not belowthe blink
        else:
            if counter >= eye_AR_consec_frame:
                total += 1
            #reset the ete frame counter
            counter = 0
            # draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the frame
            cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()









