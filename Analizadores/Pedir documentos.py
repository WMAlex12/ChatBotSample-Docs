from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

# Replace with your own Azure Storage account connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=almacendocs;AccountKey=DwIGSi+kPOURIqmzu2Ho2WS9QWNoQX6QGxsoO0OITLnwZC9kMXGEeJUOjPrzPijuKEU7gj+KD4U++AStnn9Kpg==;EndpointSuffix=core.windows.net"

# Replace with the name of the container you want to download from
container_name = "ines"

# Create a BlobServiceClient using the connection string
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get a reference to the container
container_client = blob_service_client.get_container_client(container_name)

# List all blobs in the container
blob_list = container_client.list_blobs()

# ...

for blob in blob_list:
    blob_name = blob.name
    local_file_path = os.path.join("C:\\Users\\karel\\Documents\\Hackathon\\ChatBotSample-Docs\\INEDocs", blob_name)
    
    # Create a BlobClient for the specific blob
    blob_client = container_client.get_blob_client(blob_name)
    
    # Download the blob to the local file path
    with open(local_file_path, "wb") as f:
        data = blob_client.download_blob()
        data.readinto(f)
    
    print(f"Downloaded {blob_name} to {local_file_path}")