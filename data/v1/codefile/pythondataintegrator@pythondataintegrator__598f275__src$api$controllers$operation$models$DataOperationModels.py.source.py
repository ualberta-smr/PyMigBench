import json
from datetime import datetime
from typing import List

from flask_restplus import fields

from controllers.common.models.CommonModels import EntityModel, CommonModels
from controllers.integration.models.DataIntegrationModels import DataIntegrationModels
from IocManager import IocManager
from models.dao.common.Log import Log
from models.dao.operation import DataOperation
from models.dao.operation.DataOperationContact import DataOperationContact


class DataOperationIntegrationModel(EntityModel):

    def __init__(self,
                 Order: int = None,
                 Limit: int = None,
                 ProcessCount: int = None,
                 Integration=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Order: int = Order
        self.Limit: int = Limit
        self.ProcessCount: int = ProcessCount
        self.Integration = Integration


class DataOperationContactModel(EntityModel):
    def __init__(self,
                 Email: str = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Email: str = Email


class DataOperationModel(EntityModel):
    def __init__(self,
                 Id: int = None,
                 Name: str = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id: int = Id
        self.Name: str = Name


class DataIntegrationLogModel():

    def __init__(self,
                 Id: int = None,
                 Type: str = None,
                 Content: str = None,
                 LogDatetime: datetime = None,
                 JobId: int = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id = Id
        self.Type = Type
        self.Content = Content
        self.LogDatetime = LogDatetime
        self.JobId = JobId


class DataOperationModels:
    ns = IocManager.api.namespace('DataOperation', description='Data Operation endpoints',
                                  path='/api/DataOperation')

    operation_contact = IocManager.api.model('Data Operation Contact', {
        'Email': fields.String(description='Operation contact email', required=False),
    })
    operation_integration = IocManager.api.model('Data Operation Integration', {
        'Limit': fields.Integer(description='Operation code value', required=False, example=10000),
        'ProcessCount': fields.Integer(description='Operation code value', required=True, example=1),
        'Integration': fields.Nested(DataIntegrationModels.data_integration_model,
                                     description='Integration information', required=True)
    })

    create_data_operation_model = IocManager.api.model('CreateDataOperation', {
        'Name': fields.String(description='Data Operation Name', required=True),
        'Contacts': fields.List(fields.Nested(operation_contact), description='Contact Email list',
                                required=False),
        'Integrations': fields.List(fields.Nested(operation_integration), description='Integration code list',
                                    required=True),
    })

    update_data_operation_model = IocManager.api.model('UpdateDataOperation', {
        'Name': fields.String(description='Data Operation Name', required=True),
        'Integrations': fields.List(fields.Nested(operation_integration), description='Integration code list',
                                    required=True),
    })

    delete_data_operation_model = IocManager.api.model('DeleteDataOperationModel', {
        'Id': fields.Integer(description='Connection Database Id', required=True),
    })

    @staticmethod
    def get_data_operation_contact_model(data_operation_contact: DataOperationContact) -> DataOperationContactModel:

        entity_model = DataOperationContactModel(
            Email=data_operation_contact.Email,
        )
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        return result_model

    @staticmethod
    def get_data_operation_contact_models(data_operation_contacts: List[DataOperationContact]) -> List[
        DataOperationContactModel]:
        entities = []
        for data_operation_contact in data_operation_contacts:
            if data_operation_contact.IsDeleted == 0:
                entity = DataOperationModels.get_data_operation_contact_model(data_operation_contact)
                entities.append(entity)
        return entities

    @staticmethod
    def get_data_operation_result_model(data_operation: DataOperation) -> DataOperationModel:
        entity_model = DataOperationModel(
            Id=data_operation.Id,
            Name=data_operation.Name,
        )
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        integrations = []
        for data_operation_integration in data_operation.Integrations:
            entity_model = DataOperationIntegrationModel(
                Id=data_operation_integration.Id,
                Order=data_operation_integration.Order,
                Limit=data_operation_integration.Limit,
                ProcessCount=data_operation_integration.ProcessCount,
            )
            data_operation_integration_result_model = json.loads(
                json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
            integration = DataIntegrationModels.get_data_integration_model(data_operation_integration.DataIntegration)
            data_operation_integration_result_model['Integration'] = integration
            integrations.append(data_operation_integration_result_model)
        contacts = DataOperationModels.get_data_operation_contact_models(data_operation.Contacts)
        result_model['Contacts'] = contacts
        result_model['Integrations'] = integrations
        return result_model

    @staticmethod
    def get_data_operation_result_models(data_operations: List[DataOperation]) -> List[DataOperationModel]:
        entities = []
        for data_operation in data_operations:
            if data_operation.IsDeleted == 0:
                entity = DataOperationModels.get_data_operation_result_model(data_operation)
                entities.append(entity)
        return entities

    @staticmethod
    def get_pdi_logs_model(logs: List[Log]) -> List[
        DataIntegrationLogModel]:

        entities = []
        for log in logs:
            result = DataIntegrationLogModel(
                Id=log.Id,
                JobId=log.JobId,
                Type='Info' if log.TypeId == 2 else 'Error',
                Content=log.Content,
                LogDatetime=log.LogDatetime,
            )
            entity = json.loads(json.dumps(result.__dict__, default=CommonModels.date_converter))
            entities.append(entity)
        return entities
