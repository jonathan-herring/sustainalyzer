import os
from google.cloud import storage, vision
from google.cloud.vision import types

# Path to your credentials JSON file
credentials_path = 'path/to/your/credentials.json'

# Set credentials from environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

def upload_to_gcs(bucket_name, local_file_path, destination_blob_name):
    """Uploads a file to a Google Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path)

def detect_web_entities(gcs_path):
    """Uses Google Cloud Vision API to detect web entities in an image."""
    client = vision.ImageAnnotatorClient()

    image = types.Image()
    image.source.image_uri = gcs_path

    response = client.annotate_image({
        'image': image,
        'features': [{'type': vision.enums.Feature.Type.WEB_DETECTION}],
    })

    web_entities = response.web_detection.web_entities
    return web_entities

# Example usage
bucket_name = 'your-gcs-bucket-name'
local_image_path = 'path/to/your/local/image.jpg'
destination_blob_name = 'my-image.jpg'

upload_to_gcs(bucket_name, local_image_path, destination_blob_name)

gcs_path = f'gs://{bucket_name}/{destination_blob_name}'
entities = detect_web_entities(gcs_path)

# Process the web entities and extract relevant information
for entity in entities:
    print(f"Description: {entity.description}, Score: {entity.score}")
