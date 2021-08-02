import cv2 as cv
import numpy as np
# reading images
# img = cv.imread('./pictures/simple_hand.PNG')
# print(img)
# cv.imshow('Hand', img)


# capture = cv.VideoCapture(0)
# while True:
#     isTrue, frame = capture.read()
#     cv.imshow('Video', frame)
#     if cv.waitKey(20) & 0xFF==ord('d'):
#         break

# capture.release()
# cv.destroyAllWindows()

def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1]*scale)
    height = int(frame.shape[0]*scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_CUBIC)


img = rescaleFrame(cv.imread('./pictures/left_hand.jpg'))
blur1 = cv.GaussianBlur(img, (3, 3), cv.BORDER_DEFAULT)
blur2 = cv.GaussianBlur(img, (1, 177), cv.BORDER_DEFAULT)
canny = cv.Canny(img, 100, 200)
canny2 = cv.Canny(blur1, 100, 200)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray_blur = cv.cvtColor(blur1, cv.COLOR_BGR2GRAY)
contours, heirarchies = cv.findContours(
    canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
print(len(contours))
ret, thresh = cv.threshold(gray, 100, 255, cv.THRESH_BINARY)

blank = np.zeros(img.shape, dtype=np.uint8)
# cv.drawContours(blank, contours, -1, (255, 0, 0), 1)

cv.imshow('1', img)
cv.imshow('2', blur1)
cv.imshow('3', blur2)
cv.imshow('4', canny)
cv.imshow('5', canny2)
cv.imshow('6', gray)
cv.imshow('7', thresh)
cv.imshow('7.5', blank)
cv.drawContours(blank, contours, -1, (255, 0, 0), 1)
cv.imshow('8', blank)
while True:
    if cv.waitKey(20) & 0xFF == ord('d'):
        exit()
