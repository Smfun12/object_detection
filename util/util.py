from model.BoundingBox import BoundingBox
import os


def parse_annotations_and_return_true_boxes(annotation_path):
    list_of_true_boxes = []
    for txt in os.listdir(annotation_path):
        with open(annotation_path + "/" + txt) as f:
            eof = False
            img = ''
            while not eof:
                box = BoundingBox()
                line = f.readline()
                if line.startswith('Image filename'):
                    path_array = line.split('/')
                    img = path_array[len(path_array) - 1].replace('\n', '')
                if line.startswith('Original'):
                    parts = line.split(':')
                    object_class = parts[1].replace('\n', '')
                    line = f.readline()
                    coordinates = line.split(':')[1].replace(' ', '').split(')-')
                    pnt = coordinates[0].replace(" ", '').replace('(', '').replace(')', '').split(',')
                    pnt2 = coordinates[1].replace(" ", '').replace('\n', '').replace('(', '').replace(')', '').split(
                        ',')
                    first_point = (int(pnt[0]), int(pnt[1]))
                    second_point = (int(pnt2[0]), int(pnt2[1]))
                    box.point1 = first_point
                    box.point2 = second_point
                    box.object_class = object_class.replace('"', '').replace(' ', '')
                    box.img_name = img.replace('"', '')
                    list_of_true_boxes.append(box)

                if line == '':
                    eof = True

    return list_of_true_boxes
