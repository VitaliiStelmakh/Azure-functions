import azure.functions as func
import logging
from tools.fileshare_request import FileShare

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="local_test")
async def local_test(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    get_file = FileShare()
    return func.HttpResponse(str(await get_file.read_file()))
    



