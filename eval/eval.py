def calculate_ap(list_of_scores_per_images):
    overall_TP = 0
    overall_FP = 0
    for score_bb in list_of_scores_per_images:
        overall_TP += score_bb.TP
        overall_FP += score_bb.FP

    precision = overall_TP / (overall_FP + overall_TP)
    recall = precision
    return recall
