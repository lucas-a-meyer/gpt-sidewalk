import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix


# read the curb_ramp_list.json file 
with open("curb_ramp_list.json", "r") as f:
    data = json.load(f)

# load a vector with the ground truth values
ground_truth = []
for item in data:
    ground_truth.append(item["ground_truth_has_curb_ramp"])

# load a vector with the predicted values
predicted = []
for item in data:
    predicted.append(item["has_curb_ramp"])

# use sci-kit learn to calculate accuracy, precision, recall and show the confusion matrix
print(f"Accuracy: {accuracy_score(ground_truth, predicted)}")
print(f"Precision: {precision_score(ground_truth, predicted)}")
print(f"Recall: {recall_score(ground_truth, predicted)}")

# print friendly confusion matrix
print("Confusion Matrix:")
print("                 Predicted")
print("               +          -")
print(f"Actual +     {confusion_matrix(ground_truth, predicted)[0][0]}        {confusion_matrix(ground_truth, predicted)[0][1]}")
print(f"Actual -      {confusion_matrix(ground_truth, predicted)[1][0]}        {confusion_matrix(ground_truth, predicted)[1][1]}")
