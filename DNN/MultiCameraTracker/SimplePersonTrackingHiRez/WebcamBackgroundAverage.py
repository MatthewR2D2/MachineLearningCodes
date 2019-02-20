import cv2
import numpy as np

video = "vtest.avi"

cap = cv2.VideoCapture(video)
ret, frame = cap.read()

avg1 = np.float32(frame)
avg2 = np.float32(frame)

while(1):
    ret, frame = cap.read()

    cv2.accumulateWeighted(frame, avg1, 0.1)
    cv2.accumulateWeighted(frame, avg2, 0.01)

    res1 = cv2.convertScaleAbs(avg1)
    res2 = cv2.convertScaleAbs(avg2)

    cv2.imshow("image", frame)
    cv2.imshow("AVG!" , avg1)
    cv2.imshow("AVG2" , avg2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()