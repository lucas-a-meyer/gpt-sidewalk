import semantic_kernel as sk
from semantic_kernel.orchestration import sk_context
from dotenv import load_dotenv
import json
from VisionPlugin import Vision
import asyncio

async def process_images():
    # read the JSON file
    with open("curb_ramp_list.json", "r") as f:
        data = json.load(f)

    kernel = sk.Kernel()
    vision = kernel.import_skill(Vision())
    prompt = "Does this image have a curb ramp? Respond only with 'y' if it does or 'n' if it does not.\n"

    # create a counter to track progress
    counter = 0

    # iterate over the list and get the image URL
    for item in data:
        counter += 1
        print(f"Processing item {counter} of {len(data)}")
        url = item["url"]

        # Create a Semantic Kernel context with the two fields required
        # by the Vision API function: prompt and url
        variables = sk.ContextVariables()
        variables['prompt'] = prompt
        variables['url'] = url        

        # only process images that have not been processed yet
        if 'has_curb_ramp' in item:
            continue

        has_ramp = await kernel.run_async(vision['ApplyPromptToImage'], input_vars=variables)
        has_ramp = str(has_ramp).strip().lower()
        if has_ramp == "y":	
            print("Detected curb ramp")
            item['has_curb_ramp'] = True
        elif has_ramp == "n":
            print("Did not detect curb ramp")
            item['has_curb_ramp'] = False
        else:
            print(f"Unrecognized response: {has_ramp}")

    # write the list to a file
    with open("curb_ramp_list.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(process_images())