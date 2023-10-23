import cv2 #pip3 install opencv-python --upgrade

import time
import math

basket_x = 530
basket_y = 300
ball_x = []
ball_y=[]



video = cv2.VideoCapture("bb3.mp4")

# Load tracker 
tracker = cv2.TrackerCSRT_create()

# Read the first frame of the video
returned, img = video.read()

# Select the bounding box on the image
bbox = cv2.selectROI("Tracking", img, False)

# Initialise the tracker on the img and the bounding box
tracker.init(img, bbox)

def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])

    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)

    cv2.putText(img,"Tracking",(75,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

#cv2.putText(image, text, coordinates, fontFace, fontScale, color, thickness)

def goal_track(img, bbox):
   x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
   c1 = x + int(w/2)
   c2 = y + int(h/2)
   cv2.circle(img, (c1,c2), 2, (0,0,255), 5) #Ball
   cv2.circle(img, (basket_x,basket_y),2, (0,255,0), 5) #Basket
   distance = math.sqrt(((c1-basket_x)**2)+((c2-basket_y)**2))
   if distance <=20:
       cv2.putText(img, "Goal", (300, 90), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2)
   ball_x.append(c1)
   ball_y.append(c2)
   for i in range(len(basket_x)-1):
    cv2.circle(img, (ball_x[i], ball_y[i]), 2, (0,255,0), 2)
    


while True:
    
    check, img = video.read()   

    # Update the tracker on the img and the bounding box
    success, bbox = tracker.update(img)

    if success:
        drawBox(img, bbox)
    else:
        cv2.putText(img,"Lost",(75,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

    goal_track(img, bbox)

    cv2.imshow("result", img)
            
    key = cv2.waitKey(25)
    if key == 32:
        print("Stopped")
        break

video.release()
cv2.destroyALLwindows()