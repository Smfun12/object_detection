def calculate_ap_per_class(all_img_per_class):
    tp, fp, fn = 0, 0, 0
    for el in all_img_per_class:
        tp += el.TP
        fp += el.FP
        fn += el.FN
    precision = [tp / (tp + fp)]
    if tp == 0 and fn == 0:
        return 0
    recall = [tp / (tp + fn)]
    recall.insert(0, 0.0)  # insert 0.0 at begining of list
    recall.append(1.0)  # insert 1.0 at end of list
    mrec = recall[:]
    precision.insert(0, 0.0)  # insert 0.0 at begining of list
    precision.append(0.0)  # insert 0.0 at end of list
    mpre = precision[:]

    for i in range(len(mpre) - 2, -1, -1):
        mpre[i] = max(mpre[i], mpre[i + 1])

    i_list = []
    for i in range(1, len(mrec)):
        if mrec[i] != mrec[i - 1]:
            i_list.append(i)  # if it was matlab would be i + 1
    """
     The Average Precision (AP) is the area under the curve
        (numerical integration)
        matlab: ap=sum((mrec(i)-mrec(i-1)).*mpre(i));
    """
    ap = 0.0
    for i in i_list:
        ap += ((mrec[i] - mrec[i - 1]) * mpre[i])
    return ap


def calculate_map(list_of_scores_per_images):
    ap_per_class = {}
    all_classes = [el.classname for el in list_of_scores_per_images]
    for img_class in all_classes:
        all_img_per_class = []
        for el in list_of_scores_per_images:
            if el.classname == img_class:
                all_img_per_class.append(el)
        ap_per_class[img_class] = calculate_ap_per_class(all_img_per_class)

    return sum(ap_per_class.values()) / len(ap_per_class)
