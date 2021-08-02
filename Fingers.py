from enum import Enum
from itertools import count
from typing import List
from numpy.polynomial.polynomial import polyone

from win32gui import TPM_RIGHTALIGN
from Gesture import Gesture

import math


class FingerPos(Enum):
    Down = 0
    Up = 1
    Horizontal = 2
    Other = 3


class Orientation(Enum):
    Left = 0
    Right = 1


class Fingers:
    def __init__(self):
        self.__pinky_pos: FingerPos = 0
        self.__ring_finger_pos: FingerPos = 0
        self.__middle_finger_pos: FingerPos = 0
        self.__index_finger_pos: FingerPos = 0
        self.__hand_upside_down: bool = False

        self.__ratio_range_for_open_palm = (1.618 - 0.17, 1.618 + 0.17)

        self.orientation: Orientation = Orientation.Left
        self.allFingers: FingerPos = FingerPos.Other

        self.__curr_gesture: Gesture = Gesture.Null

        self.points = []

    def givePoints(self, points):
        counter = 0  # has a count of the number of fingers that are down
        self.points = points
        if points[20].y > points[19].y > points[18].y:
            self.__pinky_pos = FingerPos.Down
            counter -= 1
            # print(self.__pinky_pos)
        elif points[20].y < points[19].y < points[18].y:
            self.__pinky_pos = FingerPos.Up
            counter += 1

        if points[16].y > points[15].y > points[14].y:
            self.__ring_finger_pos = FingerPos.Down
            counter -= 1
            # print("ring finger down")
        elif points[16].y < points[15].y < points[14].y:
            self.__ring_finger_pos = FingerPos.Up
            counter += 1

        if points[12].y > points[11].y > points[10].y:
            self.__middle_finger_pos = FingerPos.Down
            counter -= 1
            # print("middle finger down")
        elif points[12].y < points[11].y < points[10].y:
            self.__middle_finger_pos = FingerPos.Up
            counter += 1

        if points[8].y > points[7].y > points[6].y:
            self.__index_finger_pos = FingerPos.Down
            counter -= 1
        elif points[8].y < points[7].y < points[6].y:
            self.__index_finger_pos = FingerPos.Up
            counter += 1

        if points[0].y < points[9].y:
            self.__hand_upside_down = True
        else:
            self.__hand_upside_down = False

        if counter == -4:
            if self.__isFist():
                self.__curr_gesture = Gesture.Fist
            else:
                self.__curr_gesture = Gesture.Null
        elif counter == 4:
            if self.__isRaisedHand(points):
                self.__curr_gesture = Gesture.RaisedHand
            else:
                self.__curr_gesture = Gesture.Null
        else:
            self.__curr_gesture = Gesture.Null

    def __isFist(self) -> bool:
        for each_finger_pos in [self.__pinky_pos, self.__index_finger_pos, self.__middle_finger_pos, self.__ring_finger_pos]:
            if each_finger_pos != FingerPos.Down:
                return False
        return True and not self.__hand_upside_down

   # helper method, gets the vertical distance between two points
    def __getVerticalLen(self, i1, i2, points):
        return abs(points[i1].y - points[i2].y)

    def __getDist(self, i1, i2, points):
        return math.sqrt((points[i1].y - points[i2].y)**2 + (points[i1].x - points[i2].x)**2)

    def __isRaisedHand(self, points) -> bool:
        mid = abs(points[7].y - points[6].y)
        bottom = abs(points[6].y - points[5].y)

        if not self.__ratio_range_for_open_palm[0] < bottom/mid < self.__ratio_range_for_open_palm[1]:
            return False
        mid = self.__getDist(11, 10, points)
        bottom = self.__getDist(10, 9, points)

        if not self.__ratio_range_for_open_palm[0] < bottom/mid < self.__ratio_range_for_open_palm[1]:
            return False

        mid = self.__getDist(15, 14, points)
        bottom = self.__getDist(14, 13, points)

        if not self.__ratio_range_for_open_palm[0] < bottom/mid < self.__ratio_range_for_open_palm[1]:
            return False

        mid = self.__getDist(19, 18, points)
        bottom = self.__getDist(18, 17, points)

        if not self.__ratio_range_for_open_palm[0] < bottom/mid < self.__ratio_range_for_open_palm[1]:
            return False

        return True

    def debug_isFist(self) -> bool:
        # comment out later, for debug purposes
        finger_arr_dict = {"pinky": self.__pinky_pos, "index_finger": self.__index_finger_pos,
                           "middle_finger": self.__middle_finger_pos, "ring_finger": self.__ring_finger_pos}

        val_to_return = True
        finger_arr = ["pinky", "index_finger", "middle_finger", "ring_finger"]
        for ndx,  each_finger in enumerate(finger_arr):
            each_finger_pos = finger_arr_dict[each_finger]
            if each_finger_pos != FingerPos.Down:
                print("didnt work", finger_arr[ndx])
                # print(self.__pinky_pos)
                val_to_return = False
        return val_to_return and not self.__hand_upside_down

    def getCurrentGesture(self):
        return self.__curr_gesture
