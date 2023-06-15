# Invoice-OCR

This is a simple website that gets a image of a bill, recipt or invoice from the user and list out all the items and thier prices and other details as text.

It first identifies the boundary of the bill in the image and then applies 4 point transform to get a proper image and the uses PyTesseract OCR engine to retrive the details.
