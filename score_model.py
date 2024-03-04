import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns
from azure.cosmos import CosmosClient
import os
from dotenv import load_dotenv

load_dotenv()

cosmos_endpoint = os.getenv("SIDEWALK_COSMOS_URI")
cosmos_key = os.getenv("SIDEWALK_COSMOS_KEY")
cosmos_database_name = os.getenv("SIDEWALK_COSMOS_DATABASE")
cosmos_container_name = os.getenv("SIDEWALK_COSMOS_IMAGE_CONTAINER")

client = CosmosClient(cosmos_endpoint, credential=cosmos_key)
database = client.get_database_client(cosmos_database_name)
container = database.get_container_client(cosmos_container_name)

query = "SELECT * FROM c WHERE IS_DEFINED(c.human_review_curb_ramp_label)"

# Execute the query
items = list(container.query_items(
    query=query,
    enable_cross_partition_query=True
))

# Convert the items into a pandas DataFrame
data = []
for item in items:
    data.append(item)

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data)

# keep only records where df['human_review_curb_ramp_label'] is 1 and provider is 'Google' and where df['human_review_curb_ramp_label'] is 0 and provider is Microsoft
df = df[(df['human_review_curb_ramp_label'] == 1) & (df['provider'] == 'Google') | (df['human_review_curb_ramp_label'] == 0) & (df['provider'] == 'Microsoft')]

# Extract the relevant columns
ground_truth = df["human_review_curb_ramp_label"]
predictions = df["gptv_curb_ramp"]

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
plt.savefig("ConfusionMatrix.png")
plt.show()



# Also print the model accuracy
accuracy = np.trace(cm) / float(np.sum(cm))

print(f"Accuracy: {accuracy}")

# Also print the model precision and recall for each class
precision = cm[1, 1] / sum(cm[:, 1])
recall = cm[1, 1] / sum(cm[1, :])

print(f"Precision: {precision}")
print(f"Recall: {recall}")