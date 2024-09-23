import requests
import json

url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyAXAkuLUaDFcMqI3dxyKnzLtppBHmRsaA0'

headers = {'Content-Type': 'application/json'}
data = {
    "contents": [
        {
            "parts": [
                {"text": "Explain how AI works"}
            ]
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(data))
response_json = response.json()

# Extracting the text part of the response
ai_explanation = response_json['candidates'][0]['content']['parts'][0]['text']

# Printing the AI explanation
print(ai_explanation)

