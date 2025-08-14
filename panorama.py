"""making panorama using opencv"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

def pan(store_path = None):

    cam = 0
    if(len(sys.argv) > 1):
        cam = int(sys.argv[1])

    source = cv2.VideoCapture(cam)

    winname = "panorama capture"
    cv2.namedWindow(winname,cv2.WINDOW_NORMAL)

    imgs = []
    while cv2.waitKey(1) != 27:
        hasFeed, feed = source.read()
        if not(hasFeed):
            break

        copy = feed.copy()
        cv2.putText(copy,
                   "Rotate camera slowly",
                   (10,abs(feed.shape[0]-30)),
                   cv2.FONT_HERSHEY_PLAIN,
                   1,
                   (0,255,0),
                   1)
        cv2.imshow(winname, copy)

        imgs.append(feed)
        
    
    source.release()
    cv2.destroyWindow(winname)

    #only take 10% of frames, cause they are Alot!
    ten_per = int(0.1 * len(imgs))
    imgs = imgs[::ten_per]
    
    stitcher = cv2.Stitcher_create()
    status, res = stitcher.stitch(imgs)
    if not(status):
        plt.imshow(res[:,:,::-1]); plt.show()

        if store_path:
            cv2.imwrite(store_path, res)

        return res

    else:
        print("panorama couldnt be created :(")
    
