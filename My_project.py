# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import face_recognition
import os
import cv2
from selenium import webdriver

KNOWN_FACES_DIR = "known_faces"
TOLERENCE = 0.6
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "cnn"

video = cv2.VideoCapture(0)

print("loading known faces")

known_faces = []
known_names = []

for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
        image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)

print("processing unknown faces")

while True:
    
    ret,image = video.read()
    
   # cv2.imshow('Frame',image)
    
#    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    locations = face_recognition.face_locations(image,model=MODEL)
    encodings = face_recognition.face_encodings(image,locations)
    
    
    for face_encoding,face_location in zip(encodings,locations):
        results = face_recognition.compare_faces(known_faces, face_encoding,TOLERENCE)
        match = None
        if True in results:
            match = known_names[results.index(True)]
            print(f"Match found: {match}")
            top_left = (face_location[3],face_location[0])
            bottom_right = (face_location[1],face_location[2])
            color = [0,255,0]
            cv2.rectangle(image,top_left,bottom_right,color,FRAME_THICKNESS)
            
            top_left = (face_location[3],face_location[2])
            bottom_right = (face_location[1],face_location[2]+22)
            cv2.rectangle(image,top_left,bottom_right,color,cv2.FILLED)
            cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)
        else:
            
            
            driver = webdriver.Chrome()
            driver.get("https://web.whatsapp.com/")
            driver.maximize_window()


            name = input("Enter name or group names:")
            msg = input("Enter message:")
            count = int(input("Enter count : "))


            input("Enter anything after QR code scan")

            user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
            user.click()

            msg_box = driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")

            for index in range(count):
                
                msg_box.send_keys(msg)
                driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button").click()
                
                print("Success")
            
         
        
    cv2.imshow(filename,image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
          break  
                
            
    
    
        
    
