# OMR Scanner and Test Grader using OpenCV

## 📜 Project Overview

This project is a **Python-based Optical Mark Recognition (OMR) Scanner and Test Grader** built using OpenCV. It processes scanned or captured images of multiple-choice answer sheets, identifies the marked answers, and compares them against a predefined answer key to calculate scores. The system automatically outputs the evaluated results and saves them in a designated directory.

---

## 💡 Features

- Automatically detects the test sheet using contour detection.
- Recognizes marked answers using image processing techniques.
- Compares answers against a predefined answer key.
- Calculates the final score and overlays it on the test sheet image.
- Saves the graded output into an `outputs/` directory automatically.

---

## 🛠️ Technologies Used

- **Python 3.8+**
- **OpenCV**: For image processing.
- **NumPy**: For array manipulations.
- **imutils**: For contour sorting and perspective transformation.

---

## 📂 Directory Structure
```
OMR-Scanner-and-Test-Grader/
├── images/                   # Input test sheet images
│   ├── test_01.png           # Example input image
│   ├── test_02.png           # Example input image
│   └── ...                   # Additional images
├── outputs/                  # Directory to save graded results
│   ├── output1.jpg           # Example graded output
│   ├── output2.jpg           # Example graded output
│   └── ...                   # Additional results
├── test_grader.py            # Main Python script
└── README.md                 # Project documentation
```

---

## 📦 Installation

1. Clone the repository:
```
   git clone https://github.com/vaivhavr54/OMR Scanner and Test Grader using OpenCV.git
```
``` 
   cd OMR-Scanner-and-Test-Grader
```

3. Ensure that you have test sheet images inside the `images/` directory.

---

## 🚀 Usage

1. Run the `test_grader.py` script with an image path:
  
   python test_grader.py -i images/test_01.png
  

2. The script will:
   - Process the input test sheet.
   - Calculate the score based on the predefined answer key.
   - Save the graded test image with the score overlayed in the `outputs/` directory.

---

## 🔑 Answer Key

The correct answers for the test sheets are predefined in the `ANSWER_KEY` dictionary in the script:

```python
ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}
```

- Keys represent the question number (starting from 0).
- Values represent the index of the correct option (0-based index).

You can modify the `ANSWER_KEY` to match the correct answers for your tests.

---

## 📸 Example

### Input:
**Test Sheet Image (example):**
`images/test_01.png`

### Output:
**Graded Output Image:**
Saved in `outputs/output1.jpg`, showing the test score overlayed on the sheet.

---

## 🧪 How It Works

1. **Image Preprocessing**:
   - Converts the input image to grayscale.
   - Applies Gaussian blur and edge detection to identify contours.

2. **Document Detection**:
   - Detects the largest rectangular contour to isolate the test sheet.

3. **Bubble Detection**:
   - Finds circular contours (bubbles) and groups them by questions.

4. **Answer Evaluation**:
   - Compares the filled bubble to the predefined answer key.
   - Marks correct answers in green and incorrect answers in red.

5. **Score Calculation**:
   - Calculates the percentage of correct answers.
   - Annotates the score on the graded image.

6. **Output Saving**:
   - Saves the evaluated test sheet image in the `outputs/` directory.

---

## 📌 Customization

- **Adjust the Answer Key**:
  Modify the `ANSWER_KEY` dictionary to reflect the correct answers for your test.

- **Thresholding Parameters**:
  Tune the parameters for contour detection or bubble recognition as needed:
  ```python
  thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
  ```

---

## 🤝 Contribution

Feel free to contribute to the project by submitting issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.

---

## 📧 Contact

For questions or support, please reach out to:

- **Vaibhav Rakshe**: mailto: vaibhavrakshe9220@@gmail.com

---
