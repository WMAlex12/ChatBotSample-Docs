import os
import io
import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.storage.blob import BlobServiceClient, ContainerClient

# Configuración de Cognitive Services
endpoint = "https://inextracion.cognitiveservices.azure.com/"
key = "98173045d06045b8a98452d3acdbf4d1"
model_id = "25b03e97-ffa1-4933-b590-251ffd32ed18"

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# Configuración de Storage Account
connection_string = "DefaultEndpointsProtocol=https;AccountName=almacendocs;AccountKey=DwIGSi+kPOURIqmzu2Ho2WS9QWNoQX6QGxsoO0OITLnwZC9kMXGEeJUOjPrzPijuKEU7gj+KD4U++AStnn9Kpg==;EndpointSuffix=core.windows.net"
container_name_input = "ines"
container_name_output = "inejson"

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Obtener el contenedor de entrada
container_client_input = blob_service_client.get_container_client(container_name_input)

# Obtener el contenedor de salida
container_client_output = blob_service_client.get_container_client(container_name_output)

# Crear el contenedor de salida si no existe
try:
    container_client_output.get_container_properties()
except:
    container_client_output.create_container()

    print(f"Contenedor '{container_name_output}' creado correctamente.")

# Obtener la lista de blobs en el contenedor de entrada
blobs = container_client_input.list_blobs()

for blob in blobs:
    blob_name = blob.name
    blob_client = container_client_input.get_blob_client(blob_name)

    # Descargar el archivo del blob
    blob_data = blob_client.download_blob().readall()

    # Procesar el documento con Cognitive Services
    with io.BytesIO(blob_data) as stream:
        poller = document_analysis_client.begin_analyze_document(
            model_id=model_id, document=stream
        )
        result = poller.result()

    # Crear una estructura de datos para almacenar la información que deseas en formato JSON
    data_to_store = {
        "document_type": result.model_id,
        "documents": []
    }

    for idx, document in enumerate(result.documents):
        print(f"--------Analyzing document from {blob_name}--------")

        document_info = {
            "doc_type": document.doc_type,
            "confidence": document.confidence,
            "fields": {}
        }

        for name, field in document.fields.items():
            if hasattr(field, 'value') and hasattr(field.value, 'value'):
                field_value = field.value.value
            else:
                field_value = field.content

            field_info = {
                "value_type": field.value_type,
                "value": field_value,
                "confidence": field.confidence
            }
            document_info["fields"][name] = field_info

        data_to_store["documents"].append(document_info)

    # Convertir la estructura de datos en formato JSON
    json_data = json.dumps(data_to_store, indent=4)

    # Almacenar el JSON en el contenedor de salida
    output_blob_name = f"{blob_name}_analysis.json"
    output_blob_client = container_client_output.get_blob_client(output_blob_name)

    # Subir el JSON al blob de salida
    output_blob_client.upload_blob(json_data, overwrite=True)

    print(f"Resultado guardado en '{output_blob_name}'.")
