import os
from pathlib import Path

import cv2
import torch

from eval.eval import calculate_ap
from model.BoundingBox import BoundingBox
from model.ScoreBB import ScoreBB
from util.constants import threshold, list_of_predictedBoxed, list_of_scores_per_images, color, thickness, font, \
    fontScale
from util.util import parse_annotations_and_return_true_boxes


def main(model, annotation_files, path):
    files = os.listdir(path)
    img = []
    for el in files:
        if el.endswith('.png'):
            img.append(el)
    img = [str(path + el) for el in img]
    copy_imgs = [el for el in img]
    # Inference
    results = model(img)

    list_of_results = results.pandas().xyxy

    true_boxes = parse_annotations_and_return_true_boxes(annotation_files)

    for index, el in enumerate(list_of_results):
        img = cv2.imread(copy_imgs[index])
        x_mins = el.xmin
        x_maxes = el.xmax
        y_mins = el.ymin
        y_maxes = el.ymax
        predicted_image = predict_boxes_and_draw_image(x_mins, y_mins, x_maxes, y_maxes, el.name, copy_imgs[index],
                                                       true_boxes, img)
        save_image(predicted_image, copy_imgs[index])

    print(calculate_ap(list_of_scores_per_images))


def count_tp_fp_fn(true_boxes, pnt1, pnt2, classes, counter):
    TP = 0
    FP = 0
    for true_box in true_boxes:
        xA = max(true_box.point1[0], pnt1[0])
        yA = max(true_box.point1[1], pnt1[1])
        xB = min(true_box.point2[0], pnt2[0])
        yB = min(true_box.point2[1], pnt2[1])
        # compute the area of intersection rectangle
        interArea = abs(max((xB - xA, 0)) * max((yB - yA), 0))
        if interArea != 0:
            true_area = abs((true_box.point2[0] - true_box.point1[0]) * (true_box.point2[1] - true_box.point1[1]))
            predicted_area = abs((pnt2[0] - pnt1[0]) * (pnt2[1] - pnt1[1]))
            iou = interArea / (true_area + predicted_area - interArea)
            if iou >= threshold and classes[counter] in true_box.object_class:
                TP += 1
            else:
                FP += 1
    return TP, FP


def predict_boxes_and_draw_image(x_min, y_min, x_max, y_max, classes, img_name, list_of_true_boxes, img):
    img_name = Path(img_name).name
    image = None
    if img_name == 'test-43.png':
        print()
    TP, FP = 0, 0
    predicted_box = BoundingBox()
    true_boxes = []
    for box_object in list_of_true_boxes:
        if box_object.img_name == img_name:
            true_boxes.append(box_object)
    for i in range(0, len(x_min)):
        pnt1 = (round(x_min[i]), round(y_min[i]))
        pnt2 = (round(x_max[i]), round(y_max[i]))

        result = count_tp_fp_fn(true_boxes, pnt1, pnt2, classes, i)
        TP += result[0]
        FP += result[1]

        predicted_box.point1 = pnt1
        predicted_box.point2 = pnt2
        predicted_box.object_class = classes[i]
        predicted_box.img_name = img_name
        list_of_predictedBoxed.append(predicted_box)
        list_of_scores_per_images.append(ScoreBB(img_name, TP=TP, FP=FP, FN=0, classname=classes[i]))
        cv2.rectangle(img, pnt1, pnt2, color, thickness)
        # Draw label
        org = (pnt1[0], pnt2[1] - 10)
        image = cv2.putText(img, classes[i], org, font, fontScale, color, thickness, cv2.LINE_AA)
    # cv2.imshow('dst_rt', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return image


def save_image(image, image_path):
    parent_path = Path(image_path).parent
    # if not os.makedirs(parent_path.__str__()+"/result"):
    result_directory = parent_path.__str__() + "/result"
    if not Path.exists(Path(result_directory)):
        os.makedirs(result_directory)
    result_file = os.path.join(parent_path.__str__() + '/result', Path(image_path).name)
    if image is None:
        return None
    cv2.imwrite(result_file, image)


if __name__ == '__main__':
    yolo5 = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom
    annotation_path = 'VOC2005_1/Annotations/Caltech_cars/'
    path_to_images = 'VOC2005_1/PNGImages/Caltech_cars/'
    main(yolo5, annotation_path, path_to_images)
