import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns
import json

# read the curb_ramp_list.json file 
with open("curb_ramp_list.json", "r") as f:
    data = json.load(f)

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data)

# Extract the relevant columns
ground_truth = df["ground_truth_has_curb_ramp"]
predictions = df["has_curb_ramp"]

# Compute the confusion matrix
cm = confusion_matrix(ground_truth, predictions)

# Plotting the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=["No Curb Ramp", "Has Curb Ramp"],
            yticklabels=["No Curb Ramp", "Has Curb Ramp"])
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.title('Confusion Matrix')
plt.show()
