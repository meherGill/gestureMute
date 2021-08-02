# ML libraries
import enum
from typing import List
import cv2 as cv
import mediapipe as mp

# non ml, inbuilt packages
import time
from dataclasses import dataclass

# custom libraries
from Fingers import Fingers
from Gesture import Gesture
from gesture_api import *

# for debugging
from pprint import pprint
import keyboard

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
# through hit and trial 0.65 min detection confidence gives the best results
hands = mpHands.Hands(min_detection_confidence=0.65)
# takes the video stream, arg 0 for webcam, 1 for splitcam virtual driver
# cap = cv.VideoCapture('./Videos/vid3.mp4')
cap = cv.VideoCapture(0)

# fingers class will get the landmark, and then analyse them
# fingersLeft = Fingers()  # Fingers class for left hand
# fingersRight = Fingers()  # fingers class for right hand
fingers: Fingers = Fingers()
last_gesture: Gesture = Gesture.Null  # the last gesture attempted by the user
# the amount of seconds for which the gesture has been held on by the user
seconds_for_which_gesture_on: float = 0
time_at_gesture_start: float = 0

# the number of seconds for which the gesture needs to be held by the user
THRESHOLD_FOR_GESTURE_TO_BE_VALID: float = 1.5
# how far each point can move and still be considered to be a valid gesture
# basically, we want the gesture to be valid when its held still, in place
# but pixel perfect position is impossible to be held, unless youre a robot, hence
# some room to move your gesture is allowed, which is defined by THRESHOLD_TO_MOVE
THRESHOLD_TO_MOVE: int = 30


@dataclass
class Coords:
    x: float
    y: float


coords_at_beginning: List[Coords] = [Coords(0, 0) for i in range(21)]


# for debugging purposes, to see points and numbers on our hands
def putText(x, y, text, img):
    cv_x: int = int(x * img.shape[1])
    cv_y: int = int(y * img.shape[0])
    cv.putText(img, text, (cv_x, cv_y),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 255))


# to increase responsiveness, the gesture needs to be 'near' the same x,y coordinate
def checkIfGestureStaysInSamePosition(points, img_shape, initial_coords: List[Coords] = coords_at_beginning) -> bool:
    # THRESHOLD_TO_MOVE = 20  # this will be in pixels
    # print("comes"
    for ndx, point in enumerate(points):
        # changing points from percent to pixel
        x_pixel = point.x * img_shape[1]
        y_pixel = point.y * img_shape[0]

        if not (abs(initial_coords[ndx].x - x_pixel) <= THRESHOLD_TO_MOVE
                and abs(initial_coords[ndx].y - y_pixel) <= THRESHOLD_TO_MOVE):
            # print(ndx, initial_coords[ndx], x_pixel, y_pixel)
            return False

    return True


# so that the action doesnt enable as soon the gesture appears on frame
def checkIfGestureLastsThresholdSeconds(fingers: Fingers, img, time_for_which_valid=THRESHOLD_FOR_GESTURE_TO_BE_VALID) -> str:
    global last_gesture, time_at_gesture_start, coords_at_beginning
    if (last_gesture != Gesture.Null and last_gesture == fingers.getCurrentGesture()
            and checkIfGestureStaysInSamePosition(fingers.points, img.shape, coords_at_beginning)):
        # this path means, that the current frame showcases an ongoing gesture
        #  and does not mark the beginning of a new gesture
        seconds_for_which_gesture_on = time.time() - time_at_gesture_start
        if seconds_for_which_gesture_on >= time_for_which_valid:
            last_gesture = Gesture.Null
            return 'finished'
        else:
            return 'ongoing'
    else:
        # this path implies that the current frame showcases the beginning of a new gesture
        time_at_gesture_start = time.time()
        last_gesture = fingers.getCurrentGesture()
        return 'new_gesture'


def doSomethingWith(points, img):
    # print(img.shape)
    fingers.givePoints(points)
    result: str = checkIfGestureLastsThresholdSeconds(fingers, img)
    # print(result)
    if result == 'finished':
        curr_gesture = fingers.getCurrentGesture()
        if curr_gesture == Gesture.Fist:
            print("fist for 1.5")
            toggle_mute_in_teams()
        elif curr_gesture == Gesture.RaisedHand:
            print("hand on for 1.5")
            toggle_hand_raise_in_teams()
    elif result == 'new_gesture':
        # for a new gesture, make a copy of the beginning coordinates
        # this will be used to check if the gesture remains in the same position or not
        for ndx, point in enumerate(points):
            x_pixel = point.x * img.shape[1]
            y_pixel = point.y * img.shape[0]

            coords_at_beginning[ndx].x = x_pixel
            coords_at_beginning[ndx].y = y_pixel

            # print(coords_at_beginning)
    # debug_show_outline_at_initial_coords(coords_at_beginning, img)


# for debugging
def debug_show_points(landmark, img):
    for id, lms in enumerate(landmark):
        putText(lms.x, lms.y, str(id), img)


def debug_show_outline_at_initial_coords(coords: List[Coords], img):
    for coord in coords:
        top_left = (int(coord.x - THRESHOLD_TO_MOVE),
                    int(coord.y - THRESHOLD_TO_MOVE))
        bottom_right = (int(coord.x + THRESHOLD_TO_MOVE),
                        int(coord.y + THRESHOLD_TO_MOVE))
        cv.rectangle(img, top_left, bottom_right, (0, 255, 0), 3)


while True:
    success, img = cap.read()
    if success:
        rgbimg = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        results = hands.process(rgbimg)
        landmark = results.multi_hand_landmarks
        if landmark:  # landmark will be a list of size 2. Each element will correspond towards a Hand
            # basically, if there is only one hand on the image, then it will show landmark will have size 1
            # otherwise the size will be two
            for handLms in landmark:
                # pprint(dir(handLms))
                # for each hand in landmark
                '''
                handLms.landmark is a list of items of type:
                {
                    x: float x coordinate,
                    y: float y coordinate
                    z: float z coordinate
                }
                '''
                doSomethingWith(handLms.landmark, img)
                debug_show_points(handLms.landmark, img)

                # if keyboard.is_pressed('p'):
                #     showRatioFingers(handLms.landmark)
            # mpDraw.draw_landmarks(img, landmark[0], mpHands.HAND_CONNECTIONS)
        cv.imshow('1', img)
        if cv.waitKey(5) & 0xFF == ord('c'):
            print("hmm")
            cap.release()
            exit()
    else:
        raise SystemError("webcam feed not accessible")
