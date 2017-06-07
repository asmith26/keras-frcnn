# In=XML, Out=filepath,x1,y1,x2,y2,class_name (where x1=xmin, x2=xmax)

import glob
from xml.dom import minidom

bounding_data_path_root = 'VOCdevkit/sample/VOC2012/Annotations/'
training_data_path_root = '/home/andrew/git/keras-frcnn/VOCdevkit/sample/VOC2012/JPEGImages/'

with open('VOCdevkit/sample/VOC2012/Annotation_simple.txt', 'w') as output_file:
    # loop through files - get class label
    for xml_path in glob.iglob(bounding_data_path_root + '*.xml'):
        file_name = xml_path.split("/")[-1].split(".xml")[0]
        file_path = training_data_path_root + file_name + ".jpg"

        xmldom = minidom.parse(xml_path)

        for object in xmldom.getElementsByTagName('object'):
            class_name = object.getElementsByTagName('name')[0].childNodes[0].nodeValue

            x1 = object.getElementsByTagName('xmin')[0].childNodes[0].nodeValue
            x2 = object.getElementsByTagName('xmax')[0].childNodes[0].nodeValue
            y1 = object.getElementsByTagName('ymin')[0].childNodes[0].nodeValue
            y2 = object.getElementsByTagName('ymax')[0].childNodes[0].nodeValue

            write_string = file_path + ',' + \
                           str(x1) + ',' + \
                           str(y1) + ',' + \
                           str(x2) + ',' + \
                           str(y2) + ',' + \
                           str(class_name) + '\n'
            print(write_string)
            output_file.write(write_string)
