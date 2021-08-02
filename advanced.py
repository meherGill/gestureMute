import cv2 as cv

# print(cv.data.haarcascades)
img = cv.imread('./pictures/left_hand.jpg')


gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv.imshow('gray', gray)
haar_cascade = cv.CascadeClassifier('./data/haar_hand.xml')
face_cascade = cv.CascadeClassifier('./data/haar_face.xml')

hands_rect = haar_cascade.detectMultiScale(
    gray, scaleFactor=1.01, minNeighbors=3)

face_rect = face_cascade.detectMultiScale(
    gray, scaleFactor=1.1, minNeighbors=1
)
print(hands_rect)

for (p, q, r, s) in hands_rect:
    cv.rectangle(img, (p, q), (p+r, q+s), (0, 255, 255), thickness=2)

cv.imshow('hand', img)
while True:
    if cv.waitKey(20) & 0xFF == ord('d'):
        exit()
