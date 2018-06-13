# import the necessary packages
import cv2
import imutils
from Target import Target
import OCRUtil as ocr
import Evaluator
import math

def analysis(image):
    targets = []
    # load the image, convert it to grayscale, blur it slightly,
    # and threshold it
    height = image.shape[0]
    width = image.shape[1]
    h_offset = 230
    w_offset = 58
    image_crop = image[h_offset:height - h_offset, w_offset:width - w_offset]

    gray = cv2.cvtColor(image_crop, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    cv2.namedWindow("Image1", cv2.WINDOW_NORMAL)
    cv2.imshow("Image1", thresh)

    # find contours in the thresholded image
    cnts = cv2.findContours(thresh.copy(),
                            cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE,
                            offset=(w_offset, h_offset))
    cnts = cnts[1][::-1]

    print(width)
    # loop over the contours
    count = 1
    for c in cnts:
        # compute the center of the contour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        level = int((height - cY - h_offset) / 100)
        target = Target()
        target.level = level
        target.x = cX
        target.y = cY

        number_img = image[cY - 15:cY + 22, cX - 15:cX + 15]
        number = ocr.recognise_number(number_img)
        target.number = number

        # draw the contour and center of the shape on the image
        cv2.drawContours(image, [c], -1, (0, 0, 255), 2)
        cv2.circle(image, (cX, cY), 2, (0, 0, 255), -1)
        cv2.putText(image, 'Tar '+str(count), (cX - 40, cY - 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        print('第',count,'个目标',end='')
        target.info()
        count += 1
        targets.append(target)
    return targets


image = cv2.imread("C:\\Users\\Mike\\Desktop\\1.jpg")
targets = analysis(image)
target = Evaluator.evaluate(targets)
x = target.x - 375
y = target.y - 170
print("Angle (角度制): ",math.tan(x/y)/(2*math.pi)*360)
cv2.circle(image, (375, 200), 10, (0, 0, 255), -1)
cv2.line(image, (375, 200), target.get_coordinate(), (0, 255, 255), 3, cv2.LINE_AA)
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.imshow("Image", image)
cv2.waitKey(0)


