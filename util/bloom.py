import requests

API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    print((response).json())
    return response.json()



output = query({"inputs": "How do i make this ai understand me...", })


