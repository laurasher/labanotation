import pandas as pd
import numpy as np
import json

data_root = "data/"

ballets = ["coppelia_dawn", "artifact", "raymonda"]

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


for b in ballets:
    bbox_file = f"{data_root}coppelia_dawn/vott-csv-export/coppelia_dawn-export.csv"
    df = pd.read_csv(bbox_file)

    # Whoops. Need to uniformly name images.
    df["image"] = df["image"].str.replace("coppelia_2_", "coppelia_dawn_2_")
    df["image"] = df["image"].str.replace("artifact", "artifact_none")
    df["image"] = df["image"].str.replace("raymonda", "raymonda_none")
    df["step_length"] = df["ymax"] - df["ymin"]
    df["img_staff_num"] = df["image"].str.split("_").str[3].str.split(".").str[0].values
    df["img_num"] = df["image"].str.split("_").str[2].values
    df["staff_num"] = df["img_staff_num"].astype(int) * df["img_num"].astype(int)
    df["ballet"] = b

    # Group labels of same boxes
    df = (
        df.groupby(
            [
                "image",
                "ballet",
                "xmin",
                "xmax",
                "ymin",
                "ymax",
                "staff_num",
                "step_length",
                "img_staff_num",
                "img_num",
            ]
        )["label"]
        .apply(", ".join)
        .reset_index()
    )

    # Order temporally
    df = (
        df.sort_values(by=["staff_num", "ymax"], ascending=[True, False])
        .reset_index()
        .drop(["index"], axis=1)
    )

    # Create columns for movement: body (weight distribution), height, direction
    df = pd.concat([df, df["label"].str.split(",", expand=True)], axis=1).drop(
        [2], axis=1
    )
    df["direction_movement"] = df.apply(
        lambda row: label_direction_movement(row), axis=1
    )
    df["body_movement"] = df.apply(lambda row: label_body_movement(row), axis=1)
    df["height_movement"] = df.apply(lambda row: label_height_movement(row), axis=1)
    df = df.drop([0, 1, "img_num", "img_staff_num"], axis=1)
    df_to_save = df[df["image"].str.contains(b)].drop(["image"], axis=1).reset_index()
    df_to_save = df_to_save.drop(['index'], axis=1)
    # Normalize step lengths from 0 to 1
    # df_to_save["step_length"] = (
    #     df_to_save["step_length"] - np.min(df_to_save["step_length"])
    # ) / (np.max(df_to_save["step_length"]) - np.min(df_to_save["step_length"]))
    print(df_to_save)
    print(json.dumps(json.loads(df_to_save.to_json(orient='records')), indent=4, sort_keys=True))
    df_to_save.to_csv(f"bbox_output/{b}.csv")
    with open(f"bbox_output/{b}.json", 'w') as outfile:
        json.dump(json.loads(df_to_save.reset_index().to_json(orient='records')), outfile)

# print(list(df.direction_movement.unique()))
# Import steps lookup

# Group movements into steps
