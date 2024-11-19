# import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
args = vars(ap.parse_args())

# define the answer key which maps the question number to the correct answer
ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}

# load the image, convert it to grayscale, blur it slightly, then find edges
image = cv2.imread(args["image"])
if image is None:
    print(f"[ERROR] Unable to load image '{args['image']}'. Check the file path.")
    exit()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 75, 200)

# find contours in the edge map, then initialize the contour that corresponds to the document
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
docCnt = None

# ensure that at least one contour was found
if len(cnts) > 0:
    # sort the contours according to their size in descending order
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    # loop over the sorted contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if our approximated contour has four points, assume it's the paper
        if len(approx) == 4:
            docCnt = approx
            break

if docCnt is None:
    print("[ERROR] Could not find the document contour.")
    exit()

# apply a four-point perspective transform to get a top-down bird's eye view
paper = four_point_transform(image, docCnt.reshape(4, 2))
warped = four_point_transform(gray, docCnt.reshape(4, 2))

# binarize the warped piece of paper using Otsu's thresholding
thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# find contours in the thresholded image, initialize the list of question contours
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
questionCnts = []

# loop over the contours
for c in cnts:
    # compute the bounding box of the contour
    (x, y, w, h) = cv2.boundingRect(c)
    ar = w / float(h)

    # select contours that are roughly square
    if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
        questionCnts.append(c)

# sort the question contours top-to-bottom and initialize the number of correct answers
questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]
correct = 0

# loop over each question in batches of 5
for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
    # sort the contours for the current question from left to right
    cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
    bubbled = None

    # loop over the sorted contours
    for (j, c) in enumerate(cnts):
        # create a mask for the current bubble
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)

        # apply the mask and count the non-zero pixels
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        total = cv2.countNonZero(mask)

        # determine the bubbled answer
        if bubbled is None or total > bubbled[0]:
            bubbled = (total, j)

    # compare the bubbled answer to the correct answer
    color = (0, 0, 255)
    k = ANSWER_KEY[q]

    if k == bubbled[1]:
        color = (0, 255, 0)
        correct += 1

    # draw the correct answer
    cv2.drawContours(paper, [cnts[k]], -1, color, 3)

# calculate the score
score = (correct / len(ANSWER_KEY)) * 100
print("[INFO] score: {:.2f}%".format(score))
cv2.putText(paper, "{:.2f}%".format(score), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

# save the graded paper to the outputs directory
output_dir = "outputs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

input_filename = os.path.basename(args["image"])
output_filename = os.path.join(output_dir, f"graded_{input_filename}")
cv2.imwrite(output_filename, paper)
print(f"[INFO] Graded test saved to: {output_filename}")

# display the result
cv2.imshow("Original", image)
cv2.imshow("Exam", paper)
cv2.waitKey(0)