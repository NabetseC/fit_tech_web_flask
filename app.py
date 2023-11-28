from flask import Flask, render_template, url_for, request
from tensorflow import keras 
import numpy as np
import os
import mediapipe as mp
import base64
import cv2

model= keras.saving.load_model('lstm.h5')
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence= 0.5)

def calc_angle(a,b,c):
     a = np.array(a)
     b = np.array(b)
     c = np.array(c)

     radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
     angle = np.abs(radians*180.0/np.pi)

     if angle>180:
         angle = 360-angle
     return angle

x = []
y = []

for angles in os.listdir('vid_0'):
    data = np.load('vid_0' + '/' + str(angles))
    x.append(data)
    y.append(4)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('fitech.html', pred=('HELLO WORLD'))

@app.route('/predict', methods=['POST'])
def predict():    
    """safe = np.array(x)
    safe.resize(1, 40, 8)
    print(safe.shape)
    prediction=model.predict(safe)
    print("hello :")
    if prediction[0].argmax(axis = 0) == 3:
        return 'yuh'
    else:
        return 'wrong :3' """
    
    #nparr= np.fromstring(r.data, np.uint8)

    pose_results=[]
    data= request.get_json()
    if 'images' not in data:
        return 'No image data found', 400


    images_data = data['images']
    ArrayOfAngles = []
    for image_data in images_data:
        image_data = image_data.split(',')[1]  # Remove header
        image_binary = base64.b64decode(image_data)
        nparr = np.frombuffer(image_binary, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        results = pose.process(img)

        pose_results.append(results) #not important I think
        try:
            landmarks = results.pose_landmarks.landmark

            Leftshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            Leftelbow= [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            Leftwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            Lefthip= [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            Leftknee= [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            Leftankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            Rightshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            Rightelbow= [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            Rightwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            Righthip= [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            Rightknee= [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            Rightankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            angleRightShoulder = calc_angle(Rightelbow, Rightshoulder, Righthip)
            angleRightElbow = calc_angle(Rightshoulder, Rightelbow, Rightwrist)
            angleLeftShoulder = calc_angle(Leftelbow, Leftshoulder, Lefthip)
            angleLeftElbow = calc_angle(Leftshoulder, Leftelbow, Leftwrist)
            angleLeftHip = calc_angle(Righthip, Lefthip, Leftknee)
            angleLeftLeg = calc_angle(Lefthip, Leftknee, Leftankle)
            angleRightHip = calc_angle(Lefthip, Righthip, Rightknee)
            angleRightLeg = calc_angle(Righthip, Rightknee, Rightankle)

            angles = [angleRightElbow, angleRightShoulder, angleRightHip, angleRightLeg, angleLeftElbow, angleLeftShoulder, angleLeftHip, angleLeftLeg]
            ArrayOfAngles.append(angles)
        except:
            return("body not in frame at all times")
        
    ArrayOfAngles = np.array(ArrayOfAngles)
    ArrayOfAngles.resize(1,40,8)
    pred_y=np.array(model.predict(ArrayOfAngles))
    idx = pred_y[0].argmax(axis = 0)
    
    if idx == 0:
        return 'good jab'
    elif idx == 1:
        return 'bad jab - knee lvl lack'
    elif idx == 2:
        return 'bad jab - rotation lack'
    elif idx == 3:
        return 'good rest'
    elif idx == 4:
        return 'bad rest'
    elif idx == 5:
        return 'good upper cut'
    elif idx == 6:
        return 'bad upper cut - knee lvl lack'
    elif idx == 7:
        return 'bad upper cut - rotation lack'
    elif idx == 8:
        return 'good straight'

    return("didn't find match")
    



if __name__ == "__main__":
    app.run(debug=True)