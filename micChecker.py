import cv2 as cv
import mediapipe as mp
import keyboard


def check_cam_by_index(i):
    cap = cv.VideoCapture(i)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()


def check_multiple():
    for i in range(-1, 10):
        try:
            print(f'checking camera #{i}')
            check_cam_by_index(i)
        except:
            continue


check_multiple()
cap = cv.VideoCapture(1)
while True:
    _, frame = cap.read()
    cv.imshow('1', frame)
    if cv.waitKey(5) & 0xFF == ord('c'):
        print(frame)
        cap.release()
        exit()
exit()
