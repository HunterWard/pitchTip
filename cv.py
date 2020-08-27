"""
cv.py

File to process pitching video

"""
import numpy as np
import cv2
import glob

# Returns list of matrices
def processVideo(video, show=False):
    cap = cv2.VideoCapture(video)

    # varThreshold could be higher to remove more
    # Catcher/Batter are hard to get rid of
    fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=240, history=12)

    descriptors=[]
    running = True

    while(running):
        try:
            # Read in frame
            ret, frame = cap.read()
            if np.shape(frame) == ():
                break

            # Background removal
            imgMasked = fgbg.apply(frame)
            
            # Create mask to just detect features around pitcher
            mask = np.zeros(imgMasked.shape[:2], dtype=np.uint8)
            cv2.rectangle(mask, (350,85), (825,720), (177), thickness = -1)
            
            # Feature detection
            desget = cv2.SIFT_create()
            fast = cv2.FastFeatureDetector_create(125, True)
            kp = fast.detect(imgMasked,mask)

            # Compute descriptors
            a, des = desget.compute(imgMasked, kp)
            descriptors.append(des)

            if show:
                P = cv2.drawKeypoints(imgMasked,kp, None, color=(0,0,255))
                cv2.imshow(video, P)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except:
            print("Error or unexpected EOF")
            running = False

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

    if descriptors[0] == None:
        descriptors.pop(0)

    return descriptors
