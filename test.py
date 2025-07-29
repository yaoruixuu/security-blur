import requests
import json

url = "https://api-image-705613906606.us-central1.run.app//process_gcs"
data = {"gcs_uri": "your bucket uri"}

response = requests.post(url, json=data)
with open("sample_sanitized_output.json", "w") as f:
    f.write(json.dumps(response.json(), indent = 4))

print(response)


url = "https://api-image-705613906606.us-central1.run.app//summarize"
data = {"prompt": response.json()["sanitized_text"]}

response = requests.post(url, json=data)
with open("sample_summary_output.json", "w") as f:
    f.write(json.dumps(response.json(), indent = 4))

print(response)
