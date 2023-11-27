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
    
    for image_data in images_data:
        image_data = image_data.split(',')[1]  # Remove header
        image_binary = base64.b64decode(image_data)
        nparr = np.frombuffer(image_binary, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        print(img)
        print(type(img))
        results = pose.process(img)
        pose_results.append(results)
    try: 
        print(":3")
    except:
        print("error!")
    return("works")
    



if __name__ == "__main__":
    app.run(debug=True)