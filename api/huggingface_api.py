import requests

from config import HF_API_URL, HF_TOKEN

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# stop repeated failed API calls
api_failed = False


def detect_emotion(image_path):

    global api_failed

    # if API already failed once
    # don't call again
    if api_failed:
        return "Neutral"

    try:

        with open(image_path, "rb") as f:

            data = f.read()

        response = requests.post(
            HF_API_URL,
            headers=headers,
            data=data,
            timeout=10,
        )

        result = response.json()

        if isinstance(result, list):

            return result[0]["label"]

        return "Neutral"

    except Exception as e:

        print("HuggingFace API Failed Once:", e)

        # disable future API calls
        api_failed = True

        return "Neutral"