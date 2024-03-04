import os
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv
from uuid6 import uuid7

load_dotenv()

storage_connection_string = os.getenv("SIDEWALK_STORAGE_CS")   
storage_container_name = "sidewalk-images"
cosmos_endpoint = os.getenv("SIDEWALK_COSMOS_URI")
cosmos_key = os.getenv("SIDEWALK_COSMOS_KEY")
cosmos_database_name = os.getenv("SIDEWALK_COSMOS_DATABASE")
cosmos_container_name = os.getenv("SIDEWALK_COSMOS_IMAGE_CONTAINER")

# Initialize the Blob service client
blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
container_client = blob_service_client.get_container_client(storage_container_name)

# Initialize the Cosmos DB client
cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)
database = cosmos_client.get_database_client(cosmos_database_name)
container = database.get_container_client(cosmos_container_name)

# Function to insert a blob record into Cosmos DB
def insert_blob_record(blob_name):
    print(f"Processing record {blob_name}")

    # get directory
    directory = blob_name.split('/')[0]
    filename = blob_name.split('/')[1]

    if directory == "streetside":
        provider = "Microsoft"
        service = "Streetside"
    if directory == "street-view":
        provider = "Google"
        service = "Street View"

    # if blob_name contains NoCurbRamp, then human_review_curb_ramp_label = 0, else 1
    if "NoCurbRamp" in blob_name:
        label = 0
    else:
        label = 1

    # generate an uuid7 for the id
    id = str(uuid7())

    base_url = "https://gptsidewalk.blob.core.windows.net/sidewalk-images/"

    blob_record = {
        "id": id,
        "original_file_name": filename,
        "image_url": base_url + blob_name,
        "provider": provider,
        "service": service,
        "human_review_curb_ramp_label": label
    }

    container.upsert_item(blob_record)

# Loop through each blob in the container and insert a record into Cosmos DB
i = 0
for blob in container_client.list_blobs():
    i += 1
    insert_blob_record(blob.name)
    print(f"Inserted record for blob: {blob.name}")

print(f"Processed {i} records")