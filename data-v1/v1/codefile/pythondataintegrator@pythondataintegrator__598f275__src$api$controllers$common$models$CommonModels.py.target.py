import json
import traceback
from datetime import datetime

from flask_restx import fields

from IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.exceptions.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger


@IocManager.api.errorhandler(OperationalException)
def handle_operational_exception(exception):
    separator = '|'
    default_content_type = "application/json"
    mime_type_string = "mimetype"
    """Return JSON instead of HTML for HTTP errors."""
    IocManager.injector.get(DatabaseSessionManager).rollback()
    # start with the correct headers and status code from the error
    exception_traceback = traceback.format_exc()
    output = separator.join(exception.args)
    # replace the body with JSON
    # response = json.dumps()
    output_message = "empty"
    if output is not None and output != "":
        output_message = output
    trace_message = "empty"
    if exception_traceback is not None and exception_traceback != "":
        trace_message = exception_traceback
    IocManager.injector.get(SqlLogger).error(f'Operational Exception Messsage:{output_message} - Trace:{trace_message}')
    return {
        "result": "",
        "isSuccess": "false",
        "message": output
    }, 400, {mime_type_string: default_content_type}


# @IocManager.api.errorhandler(Exception)
# def handle_error(error):
#     return CommonModels.get_error_response(message=error)

class CommonModels:
    SuccessModel = IocManager.api.model('SuccessModel', {
        'IsSuccess': fields.Boolean(description='Service finished operation with successfully', default=True),
        'Message': fields.String(description='Service result values', default="Operation Completed"),
        'Result': fields.Raw(description='Service result values'),
    })

    def date_converter(o):
        if isinstance(o, datetime):
            return o.__str__()
    @staticmethod
    def get_response(result=None, message=None):
        return {'Result': result, 'Message': message}

    @staticmethod
    def get_error_response(message):
        return {"IsSuccess": False, 'Message': message}


class EntityModel:
    def __init__(self,
                 Id: int = None,
                 ):
        self.Id: int = Id
