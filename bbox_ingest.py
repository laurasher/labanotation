import pandas as pd
import numpy as np
import json
from utilFunctions import *

pd.set_option("display.max_rows", 500, "display.max_columns", 500)
pd.set_option("display.expand_frame_repr", False)

data_root = "data/"

ballets = ["coppelia_dawn", "artifact", "raymonda", "sleepingbeauty_bluebird", "songs"]

for b in ballets:
    bbox_file = f"{data_root}coppelia_dawn/vott-csv-export/coppelia_dawn-export.csv"
    df = pd.read_csv(bbox_file)
    # print(df)
    # Whoops. Need to uniformly name images.
    df["image"] = df["image"].str.replace("coppelia_2_", "coppelia_dawn_2_")
    df["image"] = df["image"].str.replace("artifact", "artifact_none")
    df["image"] = df["image"].str.replace("raymonda", "raymonda_none")
    df["image"] = df["image"].str.replace("songs", "songs_none")
    # df["image"] = df["image"].str.replace("korobushka", "korobushka_none")

    # Isolate selected ballet
    df = df[df["image"].str.contains(b)].reset_index()
    df["step_length"] = df["ymax"] - df["ymin"]
    df["img_staff_num"] = df["image"].str.split("_").str[3].str.split(".").str[0].values
    df["img_num"] = df["image"].str.split("_").str[2].values
    df["staff_num"] = df.apply(lambda row: label_staff_num(row, b), axis=1)
    df["ballet"] = b
    df = df[['image','ballet','xmin','ymin','xmax','ymax','label','step_length','img_num','img_staff_num','staff_num']]

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
    df = pd.concat([df, df["label"].str.split(",", expand=True)], axis=1)
    df["direction_movement"] = df.apply(
        lambda row: label_direction_movement(row), axis=1
    )
    df["body_movement"] = df.apply(lambda row: label_body_movement(row), axis=1)
    df["height_movement"] = df.apply(lambda row: label_height_movement(row), axis=1)
    df_w_measures = df

     # Group by measures
    measures = df[df["label"].str.contains("measure")]
    measures["measure_num"] = measures["label"].str.split('_').str[1]
    measures = measures[
        [
            "ballet",
            "ymin",
            "ymax",
            "label",
            "step_length",
            "img_num",
            "img_staff_num",
            "staff_num",
            "measure_num"
        ]
    ]
    df = df[~df["label"].str.contains("measure")]
    df["measure_num"] = df.apply(lambda row: label_measures(row, measures), axis=1)
    # print(df_w_measures)
    df = df.drop([0, 1, "img_num", "img_staff_num"], axis=1)
    df_to_save = df[df["image"].str.contains(b)].reset_index()
    # .drop(["image"], axis=1).reset_index()
    df_to_save = df_to_save.drop(['index'], axis=1)

    # Normalize step lengths from 0 to 1. Only doing this within a ballet.
    df_to_save["step_length"] = (
        df_to_save["step_length"] - np.min(df_to_save["step_length"])
    ) / (np.max(df_to_save["step_length"]) - np.min(df_to_save["step_length"]))


    df_to_save = df_to_save[[ "image",
                "ballet",
                "ymin",
                "ymax",
                "staff_num",
                "step_length",
                "label",
                "direction_movement",
                "body_movement",
                "height_movement",
                "measure_num"]]
    
    df_to_save = df_to_save.dropna()
    print(df_to_save)
    df_to_save.to_csv(f"bbox_output/{b}.csv")
    print(f"bbox_output/{b}.csv")
    with open(f"bbox_output/{b}.json", 'w') as outfile:
        json.dump(json.loads(df_to_save.reset_index().to_json(orient='records')), outfile)

