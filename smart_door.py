# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 15:27:51 2020

@author: maxki
"""


import flask
from flask import render_template
from flask import request 
from flask import jsonify
from flask import Flask, Blueprint
from werkzeug.contrib.fixers import ProxyFix
import face_recognition
import dlib
import cv2
import numpy as np
import matplotlib.pyplot as plt

pic_name = ""
def capture(pic_name):
    video_capture = cv2.VideoCapture(0)
    if video_capture.isOpened(): # try to get the first frame
        is_capturing, frame = video_capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    # makes the blues image look real colored
        webcam_preview = plt.imshow(frame) 
        webcam_preview.figure.savefig('C://Users//maxki//AI//face_recognition-master//examples//people_i_know//'+pic_name+'.png')
        #webcam_preview.figure.savefig('C://Users//maxki//AI//face_recognition-master//examples//people_i_know//From_flask.png')
       
        #webcam_preview.savefig('YL01.png')
        #save_face = plt.figure(frame)
    else:
        is_capturing = False
#pic_encoding b4 check_face
def pic_encoding(pic_name):
    pic_img = face_recognition.load_image_file('C://Users//maxki//AI//face_recognition-master//examples//people_i_know//'+pic_name+'.png')
    any_face_encoding = face_recognition.face_encodings(pic_img)[0]  
    return any_face_encoding
#face real time check function block
def check_face(pic_name):
    known_face_encodings = [
    #obama_face_encoding,
    #biden_face_encoding,
    #Max_face_encoding,
    #Alicia_face_encoding
    pic_encoding(pic_name),
    pic_encoding("obama"),
    pic_encoding("Max")
    pic_encoding("Alicia")
    ]
    known_face_names = [
    #"Barack Obama",
    #"Joe Biden",
    pic_name,
    "Obama",
    "Max",
    "Alicia"
    ]
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    #reopen video
    video_capture = cv2.VideoCapture(0)
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    face_names.append(name)
        process_this_frame = not process_this_frame
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        # Display the resulting image
        cv2.imshow('Video', frame)
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    #capture()
    return "<h1>Hello Flask!</h1>"



@app.route('/hello/<name>')
def hello(name=None):
    capture(name)
    return render_template('hello.html', name=name)

@app.route('/whois/<name>')
def whois(name=None):
    check_face("Max")
    return render_template('hello.html', name=name)

app.run()