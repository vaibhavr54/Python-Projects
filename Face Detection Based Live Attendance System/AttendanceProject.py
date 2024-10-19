import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import threading
import tkinter as tk

# Path to the image dataset
path = r'Face-recognition-Attendance-System-Project-main\Images_Attendance'
images = []
classNames = []

# Load the images and extract class names
def load_images_from_folder():
    global images, classNames
    images.clear()
    classNames.clear()
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(f"Loaded images: {classNames}")

# Function to encode all faces in the dataset
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if len(encodes) > 0:
            encodeList.append(encodes[0])
        else:
            print(f"Warning: No face found in image")
    return encodeList

# Function to mark attendance in the CSV file
def markAttendance(name):
    with open(r'Face-recognition-Attendance-System-Project-main\Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            time_now = datetime.now()
            tString = time_now.strftime('%H:%M:%S')
            dString = time_now.strftime('%d/%m/%Y')
            f.writelines(f'\n{name},{tString},{dString}')

# Process frames in a separate thread
def process_frames(cap, encodeListKnown):
    face_data = {}  # Store face position and time
    timeout = 5  # Number of frames to keep face after disappearing
    threshold = 0.6  # Face distance threshold for recognition

    while True:
        success, img = cap.read()

        if not success:
            break

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        recognized_faces = []

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex] and faceDis[matchIndex] < threshold:
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                # Track recognized face
                recognized_faces.append(name)

                # Store face location and time for persistence
                face_data[name] = {'loc': (x1, y1, x2, y2), 'frames': timeout}

                # Draw rectangle and label
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                markAttendance(name)

        # Update face_data and handle faces no longer detected
        faces_to_remove = []
        for name in list(face_data.keys()):
            if name not in recognized_faces:
                face_data[name]['frames'] -= 1  # Reduce persistence count
                if face_data[name]['frames'] <= 0:
                    faces_to_remove.append(name)  # Mark for removal

        # Remove faces that are no longer in the frame
        for name in faces_to_remove:
            del face_data[name]

        # Keep showing detected faces until their persistence runs out
        for name, data in face_data.items():
            x1, y1, x2, y2 = data['loc']
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        # Display the webcam feed
        cv2.imshow('webcam', img)
        
        # Exit on pressing Enter or closing the window
        if cv2.waitKey(10) == 13 or cv2.getWindowProperty('webcam', cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to register a new face and save it to the dataset
def register_new_face():
    cap = cv2.VideoCapture(0)
    face_saved = False  # Track if face has been saved

    while True:
        success, img = cap.read()
        cv2.imshow('Register Face - Press "s" to save', img)
        
        # Press 's' to save the current frame as a new face
        if cv2.waitKey(1) & 0xFF == ord('s'):
            name = input("Enter the name for the new face: ")
            if name:
                img_path = os.path.join(path, f"{name}.jpg")
                cv2.imwrite(img_path, img)
                print(f"Saved {name}'s image as {img_path}")
                face_saved = True  # Mark the face as saved
                break

        # Press 'q' to quit without saving
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close the webcam window automatically after saving
    if face_saved:
        cap.release()
        cv2.destroyAllWindows()
        # Reload images and encodings after registration
        load_images_from_folder()
        print("Re-encoding faces after registering new face.")

# Start webcam capture and process frames
def start_recognition():
    encodeListKnown = findEncodings(images)
    cap = cv2.VideoCapture(0)
    threading.Thread(target=process_frames, args=(cap, encodeListKnown)).start()

# GUI for user interaction
def gui_interface():
    root = tk.Tk()
    root.title("Face Recognition Attendance System")

    tk.Label(root, text="Face Recognition Attendance System", font=("Arial", 16)).pack(pady=10)

    start_btn = tk.Button(root, text="Start Recognition", command=start_recognition, font=("Arial", 12))
    start_btn.pack(pady=5)

    register_btn = tk.Button(root, text="Register New Face", command=register_new_face, font=("Arial", 12))
    register_btn.pack(pady=5)

    quit_btn = tk.Button(root, text="Quit", command=root.quit, font=("Arial", 12))
    quit_btn.pack(pady=5)

    root.mainloop()

# Main program
if __name__ == "__main__":
    load_images_from_folder()  # Initial load of images from folder
    gui_interface()
