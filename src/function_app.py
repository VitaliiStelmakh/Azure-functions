from tools.ai_document_recog import AiDocumentRecog
from tools.fileshare_request import FileShare 
from tools.blolb_push import PushToBlob
import azure.functions as func
import logging


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="local_test")
async def local_test(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    get_file = FileShare()
    ai_recog = AiDocumentRecog()
    blob_push = PushToBlob()
    dict_of_files = await ai_recog.process_request(await get_file.read_file())
    is_file_pusshed = await blob_push.push_to_blob(dict_of_files)
    if is_file_pusshed is True:
        return func.HttpResponse("Documents processed and results stored successfully!")
    else: 
        return func.HttpResponse(f"Unexpected error ocured error: {is_file_pusshed}")


