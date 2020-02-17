import json
import cv2
import numpy as np
import base64
from urllib.parse import parse_qs

def hello(event, context):
    reqBody = parse_qs(event["body"])
    print('reqBody: ', reqBody["image"][0])
    pixels = read_base64_image(reqBody["image"][0])

    modelFile = "models/opencv_face_detector_uint8.pb"
    configFile = "models/opencv_face_detector.pbtxt"
    net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

    # pixels = cv2.imread('student023.jpg')
    faces = detect_with_dnn(net, pixels)

    response = {
        "statusCode": 200,
        "body": json.dumps(faces)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

def detect_with_dnn(net, pixels):
    (h, w) = pixels.shape[:2]
    frameOpencvDnn = cv2.resize(pixels, (300, 300))
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 177, 123], False, False)

    # perform face detection
    net.setInput(blob)
    detections = net.forward()

    faces = []
    # Iterate detection
    for i in range(detections.shape[2]):
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (x1, y1, x2, y2) = box.astype("int")
        confidence = detections[0, 0, i, 2]
        if (confidence > 0.22): # filter out only bigger than 20% confident (origin 16.5%)
            # cv2.rectangle(pixels, (x1.item(), y1.item()), (x2.item(), y2.item()), (0,0,255), 2)
            faces.append([x1.item(), y1.item(), x2.item(), y2.item()])
    
    return faces

def read_base64_image(base64_string):
    # https://stackoverflow.com/questions/2941995/python-ignore-incorrect-padding-error-when-base64-decoding
    base64_string += "=" * ((4 - len(base64_string) % 4) % 4) #ugh

    decoded = base64.b64decode(base64_string)
    nparr = np.fromstring(decoded, np.uint8)

    return cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)