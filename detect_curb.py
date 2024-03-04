from dotenv import load_dotenv
from azure.cosmos import CosmosClient
import asyncio
import os
from openai import AzureOpenAI

def detect_curb_ramp(client, model, prompt, url):

        response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url","image_url": {"url": url,
            },},],}],
        max_tokens=4000,
        )    

        return response.choices[0].message.content

async def process_images():
    # Read documents from cosmos
    # Initialize Cosmos client
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

    prompt = "Does this image have a curb ramp? Respond only with 'y' if it does or 'n' if it does not.\n"

    # create a counter to track progress
    counter = 0

    openai_api_key = os.getenv("OPENAI_SDC_API_KEY")
    openai_endpoint = os.getenv("OPENAI_SDC_ENDPOINT")
    openai_model = "gpt-4-vision"
    openai_client = AzureOpenAI(azure_endpoint=openai_endpoint,
                                api_key=openai_api_key,
                                api_version="2023-12-01-preview")    

    # iterate over the list and get the image URL
    for item in items:
        counter += 1
        print(f"Processing item {counter}")
        url = item["image_url"]

        if 'has_curb_ramp' in item:
            continue

        label = item["human_review_curb_ramp_label"]

        has_ramp = detect_curb_ramp(openai_client, openai_model, prompt, url)
        has_ramp = str(has_ramp).strip().lower()

        if has_ramp == "y":	
            print(f"Detected curb ramp for image labeled {label}")
            item['gptv_curb_ramp'] = 1
        elif has_ramp == "n":
            print(f"Did not detect curb ramp for image labeled {label}")
            item['gptv_curb_ramp'] = 0
        else:
            print(f"Unrecognized response: {has_ramp}")

        # Update the Cosmos DB record
        container.upsert_item(item)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(process_images())