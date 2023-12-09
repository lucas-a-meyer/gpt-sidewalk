from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI()

def parse_json_answer(str_response: str) -> bool:
    # remove ```json\n``` from start of string
    str_response = str_response[7:]
    # remove ``` from end of string
    str_response = str_response[:-3]
    # remove \n from string
    str_response = str_response.replace("\n", "")

    # read the has_curb_ramp value from the json string
    json_response = json.loads(str_response)
    has_curb_ramp = json_response["has_curb_ramp"]
    return has_curb_ramp


def gpt_detect_curb(url: str) -> str:
    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Can wheelchair users coming from the road easily access the sidewalk without a bump? Respond with a JSON object with a boolean value for the key 'has_curb_ramp'"},
                {"type": "image_url", "image_url": {"url": f"{url}"}},
        ],
        }
    ],
    max_tokens=300,
    )
    return response.choices[0].message.content

def get_curb_ramp_image_url(url: str) -> bool:

    response = gpt_detect_curb(url)

    # try to parse the answer
    try:
        has_ramp = parse_json_answer(response)
    except:
        # try again
        response = gpt_detect_curb(url)
        try:
            has_ramp = parse_json_answer(response)
        except:
            # try one more time
            response = gpt_detect_curb(url)
            has_ramp = parse_json_answer(response)
    
    return has_ramp

if __name__ == "__main__":
    # read the JSON file
    with open("curb_ramp_list.json", "r") as f:
        data = json.load(f)

    # create a counter to track progress
    counter = 0

    # iterate over the list and get the image URL
    for item in data:
        counter += 1
        print(f"Processing item {counter} of {len(data)}")
        url = item["url"]
        has_ramp = get_curb_ramp_image_url(url)
        item["has_curb_ramp"] = has_ramp

    # write the list to a file
    with open("curb_ramp_list.json", "w") as f:
        json.dump(data, f, indent=4)