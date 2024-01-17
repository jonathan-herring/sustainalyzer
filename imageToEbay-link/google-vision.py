import os
import glob
from google.cloud import storage, vision
from google.cloud.vision import types

# Path to your credentials JSON file
credentials_path = '/lib/sustainalyzer/image->ebay-link/plexiform-crane-411108-c2e2654f5576.json'

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

# Get the most recent image file from the server
list_of_files = glob.glob('/lib/sustainalyzer/uploads')
latest_image = max(list_of_files, key=os.path.getctime)

# Example usage
bucket_name = 'sustainalyzer'  # Replace with your actual bucket name
destination_blob_name = os.path.basename(latest_image)

upload_to_gcs(bucket_name, latest_image, destination_blob_name)

gcs_path = f'gs://{bucket_name}/{destination_blob_name}'
entities = detect_web_entities(gcs_path)

# Process the web entities and extract relevant information
for entity in entities:
    print(f"Description: {entity.description}, Score: {entity.score}")
