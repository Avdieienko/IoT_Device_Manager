import numpy as np
import cv2
import time
import datetime
import threading
import awsManager as aws
import helpers
import os

# Create temp_storage folder if not exist
helpers.create_temp_storage()

alg = "haarcascade_frontalface_default.xml"
haar_cascade = cv2.CascadeClassifier(alg)

#Setting up a frame parametres
count = 1
prev_frame = None
cap = cv2.VideoCapture(0)
frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

client = aws.configure_aws_user()
tags = aws.configure_IoT_device(client)
credentials = aws.assume_role(client, "test" ,tags, "IoTDeviceWriteVideo")
role_start = time.time()
role_end = 1190
out = None
# Date for the video name; should be set for threading
date = None

def renew_credentials():
    global credentials, credentials_thread
    credentials = aws.assume_role(client, "test" ,tags, "IoTDeviceWriteVideo")
    credentials_thread = threading.Thread(target=renew_credentials)

def save_recording():
    global date, recording_thread, credentials, tags
    cur_date = date
    os.system(f'sh ./scripts/codec_convert.sh ./temp_storage/mp4v/{cur_date}.mp4 ./temp_storage/h264/{cur_date}.mp4')
    aws.upload_to_s3_with_temporary_credentials(f"./temp_storage/h264/{cur_date}.mp4", "security-camera-videos", f"{cur_date}.mp4", credentials, tags)
    helpers.cleanup()
    recording_thread = threading.Thread(target=save_recording)

credentials_thread = threading.Thread(target=renew_credentials)
recording_thread = threading.Thread(target=save_recording)


detection = False
timer_started = False
start_time = 0
detection_stopped_time = 0
while True:
    #Time after which recording turns off if no next movements were detected
    time_to_record = 5
    count += 1
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if count % 2 == 0:
        prep_frame = cv2.GaussianBlur(grayImg, ksize=(5,5), sigmaX=0)
    if prev_frame is None:
        prev_frame = prep_frame
        continue
    #Face parametres
    face = haar_cascade.detectMultiScale(grayImg,1.3,4)
    #Difference between previous frame and current
    dif_frame = cv2.absdiff(prev_frame, prep_frame)
    #Setting previous frame to be current frame
    prev_frame = prep_frame
    #Preparing frame for better detection
    dif_frame = cv2.dilate(dif_frame, np.ones((5, 5)),1)
    thresh = cv2.threshold(dif_frame, 20, 255, type=cv2.THRESH_BINARY)[1]
    #Taking contours of the movements
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #Finding the contour with the biggest shape to draw only it
    val = 0
    (x, y, w, h) = (0,0,0,0)
    g=0
    for i in contours:
        max_val = cv2.contourArea(i)
        #Skip small objects
        if max_val < 500:
            continue
        g = 1
        if max_val>val:
            (x, y, w, h) = cv2.boundingRect(i)
            val = max_val
    cv2.rectangle(img=frame, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=2)
    #Drawing face
    for (x, y, w, h) in face:
        cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (0,0,255), 2)

    # Renew credentials
    if time.time() - role_start > role_end:
        role_start = time.time()
        credentials_thread.start()

    #Check if movement/face was detected
    if g + len(face) > 0:
        #If movement was already detected before
        if detection:
            timer_started = False
        #If new movement was detected
        else:
            detection = True
            start_time = time.time()
            date = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f"./temp_storage/mp4v/{date}.mp4", fourcc, 20, frame_size)
            print("-------------\nRecording...\n-------------")
    #If no movement was detected but it was detected before
    elif detection:
        #If the recording already in proccess
        if timer_started:
            #If recording without a movement took more than 5 sec
            if time.time() - detection_stopped_time >= time_to_record:
                detection = False
                timer_started = False
                out.release()
                if(detection_stopped_time - start_time > 5):
                    recording_thread.start()
                print("-------------\nFinished\n-------------")
        #Start timer
        else:
            timer_started = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)

    cv2.imshow("Window", frame)
    if cv2.waitKey(1) == ord("q") or cv2.waitKey(1) == ord("Q"):
        if out and detection:
            out.release()
            detection_stopped_time = time.time()
            if(detection_stopped_time - start_time > 5):
                os.system(f'sh ./scripts/codec_convert.sh ./temp_storage/mp4v/{date}.mp4 ./temp_storage/h264/{date}.mp4')
                aws.upload_to_s3_with_temporary_credentials(f"./temp_storage/h264/{date}.mp4", "security-camera-videos", f"{date}.mp4", credentials, tags)
            print("-------------\nFinished\n-------------")
            print("-------------\nExiting...\n-------------")
        helpers.cleanup()
        break
cap.release()
cv2.destroyAllWindows()
