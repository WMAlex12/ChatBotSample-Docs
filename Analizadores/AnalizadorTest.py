import os
import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

endpoint = "https://inextracion.cognitiveservices.azure.com/"
key = "98173045d06045b8a98452d3acdbf4d1"
model_id = "25b03e97-ffa1-4933-b590-251ffd32ed18"

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

folder_path = "C:\\Users\\karel\\Documents\\Hackathon\\ChatBotSample-Docs\\INEDocs"
output_folder = "C:\\Users\\karel\\Documents\\Hackathon\\ChatBotSample-Docs\\JSON_INE_Docs"

# Get a list of files in the folder
file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            model_id=model_id, document=f
        )
    result = poller.result()

    for idx, document in enumerate(result.documents):
        print(f"--------Analyzing document #{idx + 1} from {file_name}--------")
        # Resto del código para imprimir los resultados

        # Crear una estructura de datos para almacenar la información que deseas en formato JSON
        data_to_store = {
            "document_type": result.model_id,
            "documents": []
        }

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

        # Construir el nombre del archivo JSON de salida
        output_file_path = os.path.join(output_folder, f"{file_name}_analysis.json")

        # Almacenar el JSON en el archivo correspondiente
        with open(output_file_path, "w") as json_file:
            json_file.write(json_data)
