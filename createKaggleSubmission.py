from __future__ import division
import glob
import json

import numpy as np
import pandas as pd

TEST1_GLOB = "fish-data/output/test_stg1/*/predictions/*"
TEST2_GLOB = "fish-data/output/test_stg2/*/predictions/*"

OUT_PATH = "fish-data/output/predictions_no_clip.csv"
#OUT_PATH = "fish-data/output/predictions_clipped.csv"

TEST_STAGE2 = False
DO_CLIP = 0.82  # value (JH used 0.82) or False
NUM_CLASSES = 8


submissions = []
for json_file in glob.glob(TEST1_GLOB):

    # Get image name (in the format required by Kaggle)
    img_name = json_file.split("/")[-1].split(".json")[0]
    if TEST_STAGE2:
        img_name = "test_stg2/{}".format(img_name)

    # Get predictions
    with open(json_file, "r") as infile:
        predictions = json.load(infile)

    row = {'ALB': 0,
           'BET': 0,
           'DOL': 0,
           'LAG': 0,
           'NoF': 0,
           'OTHER': 0,
           'SHARK': 0,
           'YFT': 0}

    num_bbox = len(predictions)
    if num_bbox == 0:
        # If no predictions, assume "NoF" (i.e. no fish class)
        row['NoF'] = 1
    else:
        class_sums_probs = {}
        total_probs = 0
        for pred in predictions:
            class_sums_probs[pred["label"]] = class_sums_probs.get(pred["label"], 0) + pred["prob"]
            total_probs += pred["prob"]

        # put predictions in 0-1
        for label, summed_prob in class_sums_probs.items():
            row[label] = summed_prob / total_probs

    # clip result (to reduce penalisation for bad predictions)
    if DO_CLIP:
        max_value = DO_CLIP
        min_value = (1 - max_value) / (NUM_CLASSES - 1)

        for label, prob in row.items():
            if prob < min_value:
                row[label] = min_value
            elif prob > max_value:
                row[label] = max_value

    row["image"] = img_name
    submissions.append(row)

pd.DataFrame(submissions).to_csv(OUT_PATH,
                      sep=',',
                      index=False,
                      encoding='utf-8')
