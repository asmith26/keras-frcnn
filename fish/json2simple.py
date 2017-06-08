import glob
import json

#map_labels = {"alb": 0, "bet": 1, "dol": 2, "lag": 3, "NoF": 4, "other": 5, "shark": 6, "yft": 7}
map_data_folders = {"alb": "ALB", "bet": "BET", "dol": "DOL", "lag": "LAG", "NoF": "NoF", "other": "OTHER",
                    "shark": "SHARK", "yft": "YFT"}

bounding_data_path_root = '../fish-data/manual_annotations/'
all_training_data_path_root = '../fish-data/train/'

with open(all_training_data_path_root+'annotations_simple.txt', 'w') as output_file:
    # loop through files - get class label
    for file_path in glob.iglob(bounding_data_path_root+'*.json'):
        class_ = file_path.split('/')[-1].split('_')[0]
        class_name = str(map_data_folders[class_])

        # open file to get data
        with open(file_path, 'r') as data_file:
            data = json.load(data_file)

            # loop through json data from each file
            for element in data:
                filename = element['filename'].split('/')[-1]
                img_path = all_training_data_path_root + map_data_folders[class_] + '/' + filename

                # if element exists get relevant elements and write to text file
                if element.get('annotations'):
                    # TODO check these are correct!?
                    xstart = int(element['annotations'][0]['x'])
                    xend = int(element['annotations'][0]['width']) + xstart
                    ystart = int(element['annotations'][0]['y'])
                    yend = int(element['annotations'][0]['height']) + ystart
                    write_string = img_path + ',' + str(xstart) + ',' + str(ystart) + ',' + str(xend) + ',' + str(
                        yend) + ',' + str(class_name) + '\n'
                    print(write_string)
                    output_file.write(write_string)