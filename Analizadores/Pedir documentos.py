from azure.storage.blob import BlobServiceClient

# Configura la información de tu cuenta de Azure Blob Storage
connection_string = "3oB9JilP76rHl5/79LfPfjEBcJeVYRbs3a06N6KnciCou2eDXUDij51pi1U/Vm6aIwkU/DCfKSlT+AStYhAUrQ=="  # Debes obtener esto desde Azure Portal

container_name = "ines"
destination_directory = r"C:\Users\karel\Documents\Hackathon\ChatBotSample-Docs\INEDocs"

# Inicializa el servicio de Blob de Azure
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

# Enumera los blobs en el contenedor
blobs = container_client.list_blobs()

for blob in blobs:
    # Crea una URL de descarga para cada archivo
    blob_url = container_client.get_blob_client(blob.name).url

    # Descarga el archivo
    with open(f"{destination_directory}/{blob.name}", "wb") as f:
        print(f"Descargando {blob.name}...")
        blob_client = container_client.get_blob_client(blob.name)
        download_stream = blob_client.download_blob()
        f.write(download_stream.readall())

print("Descarga de archivos completada.")
