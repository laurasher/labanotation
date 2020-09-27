import pandas as pd
import numpy as np
import json
import re
from utilFunctions import *

pd.set_option("display.max_rows", 500, "display.max_columns", 500)
pd.set_option("display.expand_frame_repr", False)

data_root = "data/"

# ballets = ["coppelia_dawn", "artifact", "raymonda", "sleepingbeauty_bluebird"]
ballets = ["coppelia_dawn", "artifact", "raymonda"]

# Cluster by
## Steps in one measure
## Step lengthd in one measure
## Symmetry in the body in one measure
## Diversity of movements in one measure
## Repetition in measure

for b in ballets:
    bbox_file = f"{data_root}coppelia_dawn/vott-csv-export/coppelia_dawn-export.csv"
    df = pd.read_csv(bbox_file)

    # Whoops. Need to uniformly name images.
    df["image"] = df["image"].str.replace("coppelia_2_", "coppelia_dawn_2_")
    df["image"] = df["image"].str.replace("artifact", "artifact_none")
    df["image"] = df["image"].str.replace("raymonda", "raymonda_none")

    df = df[df["image"].str.contains(b)].reset_index()
    df["step_length"] = df["ymax"] - df["ymin"]
    df["img_staff_num"] = df["image"].str.split("_").str[3].str.split(".").str[0].values
    df["img_num"] = df["image"].str.split("_").str[2].values
    df["staff_num"] = df.apply(lambda row: label_staff_num(row, b), axis=1)
    df["ballet"] = b
    df = df[
        [
            "image",
            "ballet",
            "xmin",
            "ymin",
            "xmax",
            "ymax",
            "label",
            "step_length",
            "img_num",
            "img_staff_num",
            "staff_num",
        ]
    ]

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

    # Group by measures
    measures = df[df["label"].str.contains("measure")]
    df = df[~df["label"].str.contains("measure")]
    df["measure_num"] = df.apply(lambda row: label_measures(row, measures), axis=1)

    # Order temporally
    df = (
        df.sort_values(by=["staff_num", "ymax"], ascending=[True, False])
        .reset_index()
        .drop(["index"], axis=1)
    )
    # Create columns for movement: body (weight distribution), height, direction
    # df = pd.concat([df, df["label"].str.split(",", expand=True)], axis=1).drop(
    #     [2], axis=1
    # )
    df = pd.concat([df, df["label"].str.split(",", expand=True)], axis=1)
    df["direction_movement"] = df.apply(
        lambda row: label_direction_movement(row), axis=1
    )
    df["body_movement"] = df.apply(lambda row: label_body_movement(row), axis=1)
    df["height_movement"] = df.apply(lambda row: label_height_movement(row), axis=1)
    df = df.drop([0, 1, "img_num", "img_staff_num"], axis=1)
    df_to_save = df[df["image"].str.contains(b)].reset_index()
    # .drop(["image"], axis=1).reset_index()
    df_to_save = df_to_save.drop(["index", 2], axis=1)

    # Normalize step lengths from 0 to 1
    df_to_save["step_length"] = (
        df_to_save["step_length"] - np.min(df_to_save["step_length"])
    ) / (np.max(df_to_save["step_length"]) - np.min(df_to_save["step_length"]))
    df_to_save = df_to_save.drop(
        ["xmin", "xmax", "ymin", "ymax", "label", "image"], axis=1
    )
    # Group by measure and create new dataframe for clustering
    ## Start with a simple metric, likw number of movements in each measure
    measure_count_df = (
        df_to_save.groupby(["measure_num", "ballet"])
        .size()
        .reset_index(name="movements_in_measure")
    )
    measure_count_df["measure_num"] = measure_count_df["measure_num"].astype(int)
    measure_count_df = (
        measure_count_df.sort_values(by=["measure_num"])
        .reset_index()
        .drop(["index"], axis=1)
    )
    measure_count_df = measure_count_df[
        ["ballet", "measure_num", "movements_in_measure"]
    ]
    unique_body_movements = (
        df_to_save.groupby(["measure_num", "ballet"])
        .agg(["count", "nunique"])
        .reset_index(drop=False)
        .reset_index()
    )

    tmp = pd.DataFrame(
        data={
            "measure_num": list(unique_body_movements["measure_num"].astype(int)),
            "unique_body_movements_in_measure": list(
                unique_body_movements["body_movement"]["nunique"]
            ),
            "unique_directions_in_measure": list(
                unique_body_movements["direction_movement"]["nunique"]
            ),
        }
    )
    measure_count_df = measure_count_df.merge(
        tmp, left_on="measure_num", right_on="measure_num"
    )
    measure_count_df['repetition_index'] = 1-(measure_count_df['unique_body_movements_in_measure']/measure_count_df['movements_in_measure'])
    measure_count_df['direction_diversity_index'] = (measure_count_df['unique_directions_in_measure']/measure_count_df['movements_in_measure'])

    print(measure_count_df)

    measure_count_df.to_csv(f"clustering_output/{b}_indices.csv", index=False)
    # with open(f"bbox_output/{b}.json", 'w') as outfile:
    #     json.dump(json.loads(df_to_save.reset_index().to_json(orient='records')), outfile)

# Import steps lookup

# Group movements into steps
