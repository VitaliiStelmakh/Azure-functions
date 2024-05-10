from azure.ai.formrecognizer.aio import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from os import getenv
import logging


class AiDocumentRecog:

    def __init__(self):
        endpoint = getenv('FORM_RECOGNIZER_ENDPOINT')
        api_key = getenv('FORM_RECOGNIZER_API_KEY')

        self.recogn_conn = DocumentAnalysisClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(str(api_key))
        )

    async def process_request(self, data: dict):
        """
        Push data to Azure AI Document Intelligence after get it and return as json
        data: dictionary of {name: value}
        return: dictionary with {name_of_file: {dict of returned pages}}
        """
        result = {}
        # Sends all pdf from data to be processed by ai
        for key in data.keys():
            try:
                poller = await self.recogn_conn.begin_analyze_document("prebuilt-document", data[key])
                poller_result = await poller.result()
            except Exception as err:
                logging.error(f"Unexpected exception ocurred {err}")
            # Format result string to suit json format
            result[key] = { "pages": [page.to_dict() for page in poller_result  .pages] }
        await self.recogn_conn.close()
        return result