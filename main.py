import cv2

# img = cv2.imread('images/horse.jpg')

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
classFile = 'coco.names'

with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'deploy.prototxt'
weightsPath = 'mobilenet_iter_73000.caffemodel'

net = cv2.dnn_DetectionModel(weightsPath, configPath)
# net.setInputSIze(320, 320)
net.setInputScale(1.0/127.5)
net.setInputMean(127.5)
net.setInputSwapRB(True)

while True:
    success, img = cap.read()
    classIds, confs, bbox = net.detect(img, confThreshold=0.5)

    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(img, box, color=(0, 0, 255), thickness=3)
            cv2.putText(img, classNames[classId].title(), (box[0]+10, box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255,
                                                                                                                0), 2)

    cv2.imshow('Result', img)
    cv2.waitKey(1)
