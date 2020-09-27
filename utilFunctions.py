import pandas as pd
import numpy as np
import json
import re


# Movement direction
direction_movement_dict = [
    "place",
    "right",
    "left",
    "forward",
    "backward",
    "forward_diagonal",
    "backward_diagonal",
]
# Body motion
body_movement_dict = [
    "right_arm",
    "left_arm",
    "right_body",
    "left_body",
    "right_leg",
    "left_leg",
    "right_hand",
    "left_hand",
    "right_support",
    "left_support",
    "head",
]
# Movement height
height_movement_dict = ["low", "middle", "high"]

def label_direction_movement(row):
    if row[0] is not None and row[0].strip() in direction_movement_dict:
        return row[0].strip()
    if row[1] is not None and row[1].strip() in direction_movement_dict:
        return row[1].strip()


def label_height_movement(row):
    def strip_direction(s):
        return (
            s.replace("right_arm_", "")
            .replace("left_arm_", "")
            .replace("right_body_", "")
            .replace("left_body_", "")
            .replace("right_leg_", "")
            .replace("left_leg_", "")
            .replace("right_hand_", "")
            .replace("left_hand_", "")
            .replace("right_support_", "")
            .replace("left_support_", "")
            .replace("head_", "")
            .strip()
        )

    if row[0] is not None and strip_direction(row[0]) in height_movement_dict:
        return strip_direction(row[0])
    if row[1] is not None and strip_direction(row[1]) in height_movement_dict:
        return strip_direction(row[1])


def label_body_movement(row):
    def strip_height(s):
        return s.replace("_high", "").replace("_middle", "").replace("_low", "").strip()

    if row[0] is not None and strip_height(row[0]) in body_movement_dict:
        return strip_height(row[0])
    if row[1] is not None and strip_height(row[1]) in body_movement_dict:
        return strip_height(row[1])


def label_staff_num(row, ballet):
    if ballet == "sleepingbeauty_bluebird":
        if int(row["img_num"]) == 1 and int(row["img_staff_num"]) == 1:
            return 1
        if int(row["img_num"]) == 1 and int(row["img_staff_num"]) == 2:
            return 2
        if int(row["img_num"]) == 1 and int(row["img_staff_num"]) == 3:
            return 3
        if int(row["img_num"]) == 2 and int(row["img_staff_num"]) == 1:
            return 4
        if int(row["img_num"]) == 2 and int(row["img_staff_num"]) == 2:
            return 5
        if int(row["img_num"]) == 2 and int(row["img_staff_num"]) == 3:
            return 6
        if int(row["img_num"]) == 3 and int(row["img_staff_num"]) == 1:
            return 7
        if int(row["img_num"]) == 3 and int(row["img_staff_num"]) == 2:
            return 8
        if int(row["img_num"]) == 3 and int(row["img_staff_num"]) == 3:
            return 9
    else:
        if int(row["img_num"]) == 1 and int(row["img_staff_num"]) == 1:
            return 1
        if int(row["img_num"]) == 1 and int(row["img_staff_num"]) == 2:
            return 2
        if int(row["img_num"]) == 1 and int(row["img_staff_num"]) == 3:
            return 3
        if int(row["img_num"]) == 1 and int(row["img_staff_num"]) == 4:
            return 4
        if int(row["img_num"]) == 2 and int(row["img_staff_num"]) == 1:
            return 5
        if int(row["img_num"]) == 2 and int(row["img_staff_num"]) == 2:
            return 6
        if int(row["img_num"]) == 2 and int(row["img_staff_num"]) == 3:
            return 7
        if int(row["img_num"]) == 2 and int(row["img_staff_num"]) == 4:
            return 8
        if int(row["img_num"]) == 3 and int(row["img_staff_num"]) == 1:
            return 9
        if int(row["img_num"]) == 3 and int(row["img_staff_num"]) == 2:
            return 10
        if int(row["img_num"]) == 3 and int(row["img_staff_num"]) == 3:
            return 11
        if int(row["img_num"]) == 3 and int(row["img_staff_num"]) == 4:
            return 12


def label_measures(row, measures):
    margin = 2
    res = measures[
        (
            (row["ymin"] >= measures["ymin"])
            | (row["ymin"] >= measures["ymin"] - margin)
            | (row["ymin"] >= measures["ymin"] + margin)
        )
        & (
            (row["ymax"] <= measures["ymax"])
            | (row["ymax"] <= measures["ymax"] - margin)
            | (row["ymax"] <= measures["ymax"] + margin)
        )
        & (row["staff_num"] == measures["staff_num"])
    ]
    # res = measures[ (abs(row['ymin']-measures['ymin'])<=10) & (abs(row['ymax']-measures['ymax'])<=10) & (row['staff_num']==measures['staff_num']) ]
    if not res.empty:
        return re.findall(r"\d+", res["label"].values[0])[0]