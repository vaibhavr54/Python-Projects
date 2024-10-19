# Face Recognition Based Live Attendance System Using OpenCV

## Overview
The **Face Recognition Attendance System** is a Python-based application designed to automate attendance tracking using facial recognition technology. This system captures live video from a webcam, recognizes registered faces, and marks attendance in a CSV file. It also allows for the registration of new faces, providing a seamless and efficient way to manage attendance in educational or corporate environments.

## Features
- **Real-time Face Recognition**: Identifies and recognizes registered faces using a webcam.
- **Attendance Marking**: Automatically records attendance in a CSV file with timestamps.
- **Face Registration**: Users can register new faces by capturing images and entering names.
- **Dynamic Display**: Displays recognized names in real-time as faces are detected.
- **Persistent Recognition**: Maintains recognition for a specified duration even after the face leaves the frame.

## Requirements
- Python 3.x
- OpenCV
- NumPy
- face_recognition
- tkinter (for GUI)
- A webcam

### Installation of Dependencies
You can install the required libraries using pip:

```
pip install opencv-python numpy face_recognition tkinter
```

## Installation
1. **Clone the repository**:

   ```
   git clone https://github.com/yourusername/Face-recognition-Attendance-System.git
   cd Face-recognition-Attendance-System
   ```

2. **Create a directory for images**:
   - Create a folder named `Images_Attendance` inside the project directory to store registered face images.

3. **Run the application**:
   - Execute the main script:
   ```
   python main.py
   ```
  
## Usage
1. **Start the Application**: Launch the application, and a GUI will appear.
2. **Register New Faces**:
   - Click on the "Register New Face" button.
   - A webcam feed will open. Press 's' to save the current frame as a new face. Enter a name when prompted.
   - Press 'q' to exit registration mode without saving.
3. **Start Recognition**:
   - Click on the "Start Recognition" button.
   - The application will begin recognizing faces in real-time and marking attendance.
4. **Exit**: To quit the application, click the "Quit" button in the GUI or press the Enter key while the recognition window is active.

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, feel free to fork the repository and submit a pull request. 

### To Contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature/new-feature`).
6. Open a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
