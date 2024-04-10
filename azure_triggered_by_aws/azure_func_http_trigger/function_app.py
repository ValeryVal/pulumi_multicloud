import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="azure_http_trigger_func")
def azure_http_trigger_func(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_body().decode('utf-8')
    logging.info(f'Python HTTP trigger function processed a request.{body}')

    return func.HttpResponse(
         "This HTTP triggered function executed successfully",
         status_code=200,
    )
