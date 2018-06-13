import pytesseract
import cv2


def recognise_number(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
    code = pytesseract.image_to_string(thresh, config="-psm 7")
    if code.isdigit():
        return int(code)
    else:
        return -1
