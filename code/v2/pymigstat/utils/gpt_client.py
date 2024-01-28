import json

import requests

from config import config


def get_csv(message: str):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.gpt_api_key}",
    }
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": message}],
        "temperature": 1,
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
