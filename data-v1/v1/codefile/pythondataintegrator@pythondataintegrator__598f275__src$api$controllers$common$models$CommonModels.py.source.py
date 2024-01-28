from datetime import datetime

from flask_restplus import fields

from IocManager import IocManager
from infrastructor.exceptions.OperationalException import OperationalException


@IocManager.api.errorhandler(OperationalException)
def handle_error(error):
    return CommonModels.get_error_response(message=error)

@IocManager.api.errorhandler(Exception)
def handle_error(error):
    return CommonModels.get_error_response(message=error)

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
