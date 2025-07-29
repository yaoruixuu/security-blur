# Security Level Blur

REST API uses Google Cloud Platform's Document AI OCR model to "sanitize" text based on security level. Then summarizes text with Gemini 2.5 flash using its API.

## How to create endpoints:

First steps:
Create a GCP project with Document AI enabled- docs: https://cloud.google.com/document-ai/docs/setup
Create your Document AI model (processor)- docs: https://cloud.google.com/document-ai/docs/create-processor
   
Set your GCP environment variable PROJECT_ID, LOCATION, PROCESSOR_ID in a .env file or export directly in CLI:
```
export PROJECT_ID="my-project-123"
```

Create and activate a virtual environment to isolate depencies:
```
python -m venv your_venv_name
source your_venv_name/bin/activate
```

`cd` into the Dockerfile level directory and create the docker image with the dockerfile by doing `docker build -t your-image-name:tag`

Deploy container on Google Cloud Run (docs: https://cloud.google.com/run/docs/deploying) or any other service provider

# Using the API

Test out already created endpoints on your own files in GCS buckets with the `requests` library by running `python test.py`

Endpoint: https://api-image-705613906606.us-central1.run.app

Find sample json output files of the API in `example outputs`


