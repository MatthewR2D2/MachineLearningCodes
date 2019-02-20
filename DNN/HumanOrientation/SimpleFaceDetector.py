import cv2
from tqdm import tqdm
import os
import imutils



def detectFaceOpenCVDnn(net, frame):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], False, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)
    return frame, bboxes

def get_files(dataset_path):
    print("Creating Training Data")
    paths = []
    for img in tqdm(os.listdir(dataset_path)):
        path = os.path.join(dataset_path, img)
        paths.append(path)
    return paths


imagepath = "test/"
myImages = get_files(imagepath)

faceCascade = cv2.CascadeClassifier("D:/MLDataset/CV2_Detector/data/haarcascades_cuda/haarcascade_frontalface_default.xml")

#DNN = "TF"
DNN = "CAFFE"
if DNN == "CAFFE":
    modelFile = "model/res10_300x300_ssd_iter_140000_fp16.caffemodel"
    configFile = "model/deploy.prototxt"
    net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
else:
    modelFile = "model/opencv_face_detector_uint8.pb"
    configFile = "model/opencv_face_detector.pbtxt"
    net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)


for image in myImages:
    img = cv2.imread(image)
    img = imutils.resize(img, width= 1000)
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    outOpencvDnn, bboxes = detectFaceOpenCVDnn(net, img)
    cv2.imshow("Faces", img)
    cv2.waitKey(0)


cv2.destroyAllWindows()



