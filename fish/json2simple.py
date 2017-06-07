import os
import glob

map_labels = {"alb": 0, "bet": 1, "dol": 2, "lag": 3, "NoF": 4, "other": 5, "shark": 6, "yft": 7}
map_data_folders = {"alb": "ALB", "bet": "BET", "dol": "DOL", "lag": "LAG", "NoF": "NoF", "other": "OTHER",
                    "shark": "SHARK", "yft": "YFT"}

bounding_data_path_root = '/home/ubuntu/data/fishing/bounding_boxes/'
training_data_path_root = '/home/ubuntu/data/fishing/train/'
output_file = open('/home/ubuntu/data/fishing/bounding_boxes/output/output.txt', 'a')

# loop through files - get class label
os.chdir(data_path_root)
for file in list(glob.glob('*.json')):
    class_ = file.split('_')[0]
    class_name = str(map_labels[class_])

    # open file to get data
    with open(bounding_data_path_root + file) as data_file:
        data = json.load(data_file)

        # loop through json data from each file
        for element in data:
            filename = element['filename'].split('/')[-1]
            file_path = training_data_path_root + map_data_folders[class_] + '/' + filename

            # if element exists get relevant elements and write to text file
            if element.get('annotations'):
                # TODO check these are correct!?
                xstart = int(element['annotations'][0]['x'])
                xend = int(element['annotations'][0]['width']) + xstart
                ystart = int(element['annotations'][0]['y'])
                yend = int(element['annotations'][0]['height']) + ystart
                write_string = file_path + ',' + str(xstart) + ',' + str(ystart) + ',' + str(xend) + ',' + str(
                    yend) + ',' + str(class_name) + '\n'
                print(write_string)
                output_file.write(write_string)
    data_file.close()
output_file.close()