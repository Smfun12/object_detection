import cv2

threshold = 0.6
pred_color = (255, 0, 0)
true_color = (0, 0, 255)
thickness = 1
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.3
list_of_predictedBoxed = []
list_of_scores_per_images = []
