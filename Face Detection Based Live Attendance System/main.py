import cv2
import numpy as np
import face_recognition
import os
print(os.getcwd())

imgModi = face_recognition.load_image_file(r'D:\FERUML\Face-recognition-Attendance-System-Project-main\Face-recognition-Attendance-System-Project-main\Images_Attendance\modi-image-for-InUth.jpg')
imgModi = cv2.cvtColor(imgModi, cv2.COLOR_BGR2RGB)
imgTest = face_recognition.load_image_file(r'D:\FERUML\Face-recognition-Attendance-System-Project-main\Face-recognition-Attendance-System-Project-main\Images_Attendance\narendra-modi.jpg')
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

faceloc = face_recognition.face_locations(imgModi)[0]
encodeModi = face_recognition.face_encodings(imgModi)[0]
cv2.rectangle(imgModi, (faceloc[3], faceloc[0]), (faceloc[1], faceloc[2]), (155, 0, 255), 2)

facelocTest = face_recognition.face_locations(imgTest)[0]
face_encodings_test = face_recognition.face_encodings(imgTest)
if len(face_encodings_test) > 0:
    encodeTest = face_encodings_test[0]  # Access the first encoding if available
else:
    print("No face detected in the test image.")

cv2.rectangle(imgTest, (facelocTest[3], facelocTest[0]), (facelocTest[1], facelocTest[2]), (155, 0, 255), 2)

results = face_recognition.compare_faces([encodeModi], encodeTest)
faceDis = face_recognition.face_distance([encodeModi], encodeTest)
print(results, faceDis)
cv2.putText(imgTest, f'{results} {round(faceDis[0],2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)

cv2.imshow('Modi', imgModi)
cv2.imshow('Narendra Modi', imgTest)
cv2.waitKey(0)
cv2.destroyAllWindows()