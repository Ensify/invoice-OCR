from flask import Flask, render_template,request
from imutils.perspective import four_point_transform
import matplotlib.pyplot as plt
import pytesseract
import argparse
import imutils
import cv2
import os
import re
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def im2txt(img):
    orig = cv2.imread(img)
    image = orig.copy()
    image = imutils.resize(image,width=500)
    ratio = orig.shape[1] / float(image.shape[1])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    imgTopHat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, structuringElement)
    imgBlackHat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, structuringElement)
    imgGrayscalePlusTopHat = cv2.add(gray, imgTopHat)
    gray = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

    blurred = cv2.GaussianBlur(gray,(5,5),0)
    
    edged = cv2.Canny(blurred,75,200)
    cnts = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts,key = cv2.contourArea,reverse=True)

    recipt = None

    for c in cnts:
        peri = cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c, 0.02 * peri , True)

        if len(approx) == 4:
            recipt = approx
            break

    if recipt is None:
        return ["Recipt edges not clear"]
    
    recipt = four_point_transform(orig,recipt.reshape(4,2) * ratio)
    text = pytesseract.image_to_string(cv2.cvtColor(recipt,cv2.COLOR_BGR2RGB),config="--psm 4")
    if text:
        return text.split("\n")
    return ["Recipt Not clear"]


app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def home():
    if request.method=='POST':
        image = request.files['image']
        f = image.filename
        image.save(f)
        text = im2txt(f)
        os.remove(f)
        return render_template('index.html',lines = text)
    return render_template('index.html',lines = "")



if __name__ == "__main__":
    app.run(debug=True)