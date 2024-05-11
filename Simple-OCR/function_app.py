import azure.functions as func
import logging
import os
from azure.storage.fileshare import ShareFileClient
from azure.storage.blob import BlobClient

from azure.core.credentials import AzureKeyCredential
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Environment variables
        connection_string = os.getenv('STORAGE_CONNECTION_STRING')
        file_share_name = os.getenv('FILE_SHARE_NAME')
        blob_container_name = os.getenv('BLOB_CONTAINER_NAME')
        endpoint = os.getenv('FORM_RECOGNIZER_ENDPOINT')
        api_key = os.getenv('FORM_RECOGNIZER_API_KEY')

        file_name = req.params.get('filename')
        if not file_name:
            return func.HttpResponse(
                "Please pass a filename on the query string",
                status_code=400
            )

        # Set up clients
        file_client = ShareFileClient.from_connection_string(
            conn_str=connection_string, 
            share_name=file_share_name, 
            file_path=file_name
        )
        blob_client = BlobClient.from_connection_string(
            conn_str=connection_string, 
            container_name=blob_container_name, 
            blob_name=f"{file_name}.json"  # Store results as JSON
        )
        form_recognizer_client = DocumentAnalysisClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key)
        )

        # Download PDF from file share
        download_stream = file_client.download_file()
        pdf = download_stream.readall()

        # Process PDF with Azure AI Document Intelligence
        poller = form_recognizer_client.begin_analyze_document("prebuilt-document", pdf)
        result = poller.result()

        # Convert the result to JSON
        doc_json = { "pages": [page.to_dict() for page in result.pages] }

        # Upload JSON result to Blob Storage
        blob_client.upload_blob(json.dumps(doc_json), overwrite=True)

        return func.HttpResponse("Document processed and results stored successfully!")

    except Exception as e:
        return func.HttpResponse(
            f"Error occurred: {str(e)}",
            status_code=500
        )
