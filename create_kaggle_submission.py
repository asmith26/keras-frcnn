from __future__ import division
import glob
import json

import pandas as pd

TEST1_GLOB = "fish-data/output/test_stg1/*/predictions/*"
TEST2_GLOB = "fish-data/output/test_stg2/*/predictions/*"

OUT_PATH = "fish-data/output/predictions_no_clip.csv"
OUT_PATH_CLIPPED = "fish-data/output/predictions_clipped.csv"

NUM_CLASSES = 8

def get_one_prediction(json_file, do_clip, test_stage2):
    # Get image name (in the format required by Kaggle)
    img_name = json_file.split("/")[-1].split(".json")[0]
    if test_stage2:
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
    if do_clip:
        max_value = do_clip
        min_value = (1 - max_value) / (NUM_CLASSES - 1)

        for label, prob in row.items():
            if prob < min_value:
                row[label] = min_value
            elif prob > max_value:
                row[label] = max_value

    row["image"] = img_name
    return row

def create_kaggle_subimmision(out_path, do_clip):
    submissions = []
    for json_file in glob.glob(TEST1_GLOB):
        submissions.append(get_one_prediction(json_file, do_clip, test_stage2=False))

    for json_file in glob.glob(TEST2_GLOB):
        submissions.append(get_one_prediction(json_file, do_clip, test_stage2=True))


    pd.DataFrame(submissions).to_csv(out_path,
                          sep=',',
                          index=False,
                          encoding='utf-8')

create_kaggle_subimmision(OUT_PATH, do_clip=False)
create_kaggle_subimmision(OUT_PATH_CLIPPED, do_clip=0.7)  # JH used 0.82
