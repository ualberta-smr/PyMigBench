import json
from typing import List

from flask_restplus import fields

from controllers.common.models.CommonModels import EntityModel, CommonModels
from controllers.connection.models.ConnectionModels import ConnectionModels
from IocManager import IocManager
from models.dao.integration.DataIntegration import DataIntegration


class DataIntegrationModel(EntityModel):

    def __init__(self,
                 Id=None,
                 Code=None,
                 IsTargetTruncate=None,
                 IsDelta=None,
                 CreationDate=None,
                 Comments=None,
                 IsDeleted=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id = Id
        self.Code = Code
        self.IsTargetTruncate = IsTargetTruncate
        self.IsDelta = IsDelta
        self.CreationDate = CreationDate
        self.Comments = Comments
        self.IsDeleted = IsDeleted


class DataIntegrationConnectionModel:

    def __init__(self,
                 Id: int = None,
                 SourceOrTarget: int = None,
                 DataIntegration=None,
                 Database=None,
                 File=None,
                 Connection=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id: int = Id
        self.SourceOrTarget: int = SourceOrTarget
        self.DataIntegration = DataIntegration
        self.Database = Database
        self.File = File
        self.Connection = Connection


class DataIntegrationConnectionDatabaseModel:

    def __init__(self,
                 Id: int = None,
                 Schema: str = None,
                 TableName: str = None,
                 Query: str = None,
                 *args, **kwargs):
        self.Id: int = Id
        self.Schema: str = Schema
        self.TableName: str = TableName
        self.Query: str = Query


class DataIntegrationConnectionFileModel:

    def __init__(self,
                 Id: int = None,
                 Folder: str = None,
                 FileName: str = None,
                 *args, **kwargs):
        self.Id: int = Id
        self.Folder: str = Folder
        self.FileName: str = FileName


class DataIntegrationConnectionQueueModel:
    def __init__(self,
                 Id: int = None,
                 TopicName: str = None,
                 *args, **kwargs):
        self.Id: int = Id
        self.TopicName: str = TopicName


class DataIntegrationConnectionFileCsvModel:

    def __init__(self,
                 Id: int = None,
                 HasHeader: bool = None,
                 Header: str = None,
                 Separator: str = None,
                 *args, **kwargs):
        self.Id: int = Id
        self.HasHeader: bool = HasHeader
        self.Header: str = Header
        self.Separator: str = Separator


class DataIntegrationColumnModel:

    def __init__(self,
                 Id=None,
                 ResourceType=None,
                 SourceColumnName=None,
                 TargetColumnName=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id = Id
        self.ResourceType = ResourceType
        self.SourceColumnName = SourceColumnName
        self.TargetColumnName = TargetColumnName


class DataIntegrationModels:
    ns = IocManager.api.namespace('DataIntegration', description='Data Integration endpoints',
                                  path='/api/DataIntegration')

    data_integration_connection_database_model = IocManager.api.model('DataIntegrationConnectionDatabaseModel', {
        'Schema': fields.String(description='Schema', required=False),
        'TableName': fields.String(description='TableName', required=False),
        'Query': fields.String(description='Query', required=False),
    })

    data_integration_connection_file_csv_model = IocManager.api.model('DataIntegrationConnectionFileCsvModel', {
        'HasHeader': fields.Boolean(description='HasHeader', required=False),
        'Header': fields.String(description='Header', required=False),
        'Separator': fields.String(description='Separator', required=False),
    })

    data_integration_connection_file_model = IocManager.api.model('DataIntegrationConnectionFileModel', {
        'Folder': fields.String(description='Folder', required=False),
        'FileName': fields.String(description='FileName', required=False),
        'Csv': fields.Nested(data_integration_connection_file_csv_model, description='Csv'),
    })
    data_integration_connection_queue_model = IocManager.api.model('DataIntegrationConnectionQueueModel', {
        'TopicName': fields.String(description='TopicName', required=False),
    })
    data_integration_connection_model = IocManager.api.model('DataIntegrationConnectionModel', {
        'ConnectionName': fields.String(description='ConnectionName', required=False),
        'Database': fields.Nested(data_integration_connection_database_model, description='Database connection'),
        'File': fields.Nested(data_integration_connection_file_model, description='File connection'),
        'Queue': fields.Nested(data_integration_connection_queue_model, description='Queue connection'),
        'Columns': fields.String(description='Columns'),
    })

    data_integration_model = IocManager.api.model('DataIntegrationModel', {
        'Code': fields.String(description='Operation code value', required=True),
        'SourceConnections': fields.Nested(data_integration_connection_model, description='Source Connections',
                                           required=False),
        'TargetConnections': fields.Nested(data_integration_connection_model,
                                           description='Target Connections',
                                           required=True),
        'IsTargetTruncate': fields.Boolean(description='IsTargetTruncate', required=True),
        'IsDelta': fields.Boolean(description='IsDelta'),
        'Comments': fields.String(description='Comments'),
    })

    @staticmethod
    def get_data_integration_model(data_integration: DataIntegration) -> DataIntegrationModel:
        source_list = [x for x in data_integration.Connections if x.SourceOrTarget == 0]
        source = None
        if source_list is not None and len(source_list) > 0:
            source_connection = source_list[0]
            entity_source = DataIntegrationConnectionModel(
                Id=source_connection.Id,
                SourceOrTarget=source_connection.SourceOrTarget
            )
            source = json.loads(json.dumps(entity_source.__dict__, default=CommonModels.date_converter))

            if source_connection.Database is not None:
                entity_source_database = DataIntegrationConnectionDatabaseModel(
                    Id=source_connection.Id,
                    Schema=source_connection.Database.Schema,
                    TableName=source_connection.Database.TableName,
                    Query=source_connection.Database.Query,
                )
                source_database = json.loads(
                    json.dumps(entity_source_database.__dict__, default=CommonModels.date_converter))
                source['Database'] = source_database
            if source_connection.File is not None:
                entity_source_file = DataIntegrationConnectionFileModel(
                    Id=source_connection.Id,
                    Folder=source_connection.File.Folder,
                    FileName=source_connection.File.FileName
                )
                source_file = json.loads(json.dumps(entity_source_file.__dict__, default=CommonModels.date_converter))

                if source_connection.File.Csv is not None:
                    entity_source_file_csv = DataIntegrationConnectionFileCsvModel(
                        Id=source_connection.Id,
                        HasHeader=source_connection.File.Csv.HasHeader,
                        Header=source_connection.File.Csv.Header,
                        Separator=source_connection.File.Csv.Separator,
                    )
                    source_file_csv = json.loads(
                        json.dumps(entity_source_file_csv.__dict__, default=CommonModels.date_converter))
                    source_file['Csv'] = source_file_csv
                source['File'] = source_file

            if source_connection.Queue is not None:
                entity_source_queue = DataIntegrationConnectionQueueModel(
                    Id=source_connection.Id,
                    TopicName=source_connection.Queue.TopicName,
                )
                source_queue = json.loads(json.dumps(entity_source_queue.__dict__, default=CommonModels.date_converter))
                source['Queue'] = source_queue
            source['Connection'] = ConnectionModels.get_connection_result_model(source_connection.Connection)

        target_connection = [x for x in data_integration.Connections if x.SourceOrTarget == 1][0]
        entity_target = DataIntegrationConnectionModel(
            Id=target_connection.Id,
            SourceOrTarget=target_connection.SourceOrTarget
        )
        target = json.loads(json.dumps(entity_target.__dict__, default=CommonModels.date_converter))

        if target_connection.Database is not None:
            entity_target_database = DataIntegrationConnectionDatabaseModel(
                Id=target_connection.Id,
                Schema=target_connection.Database.Schema,
                TableName=target_connection.Database.TableName,
                Query=target_connection.Database.Query,
            )
            target_database = json.loads(
                json.dumps(entity_target_database.__dict__, default=CommonModels.date_converter))
            target['Database'] = target_database
        if target_connection.File is not None:
            entity_target_file = DataIntegrationConnectionFileModel(
                Id=target_connection.Id,
                FileName=target_connection.File.FileName
            )
            target_file = json.loads(json.dumps(entity_target_file.__dict__, default=CommonModels.date_converter))

            if target_connection.File.Csv is not None:
                entity_target_file_csv = DataIntegrationConnectionFileCsvModel(
                    Id=target_connection.Id,
                    HasHeader=target_connection.File.Csv.HasHeader,
                    Header=target_connection.File.Csv.Header,
                    Separator=target_connection.File.Csv.Separator,
                )
                target_file_csv = json.loads(
                    json.dumps(entity_target_file_csv.__dict__, default=CommonModels.date_converter))
                target_file['Csv'] = target_file_csv
            target['File'] = target_file
        if target_connection.Queue is not None:
            entity_source_queue = DataIntegrationConnectionQueueModel(
                Id=target_connection.Id,
                TopicName=target_connection.Queue.TopicName,
            )
            target_queue = json.loads(json.dumps(entity_source_queue.__dict__, default=CommonModels.date_converter))
            target['Queue'] = target_queue
        target['Connection'] = ConnectionModels.get_connection_result_model(target_connection.Connection)
        columns = []
        for col in data_integration.Columns:
            entity_column = DataIntegrationColumnModel(
                Id=col.Id,
                ResourceType=col.ResourceType,
                SourceColumnName=col.SourceColumnName,
                TargetColumnName=col.TargetColumnName,
            )
            column = json.loads(json.dumps(entity_column.__dict__, default=CommonModels.date_converter))
            columns.append(column)
        entity_model = DataIntegrationModel(
            Id=data_integration.Id,
            Code=data_integration.Code,
            IsTargetTruncate=data_integration.IsTargetTruncate,
            IsDelta=data_integration.IsDelta,
            CreationDate=data_integration.CreationDate,
            Comments=data_integration.Comments,
            IsDeleted=data_integration.IsDeleted
        )

        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        if source is not None:
            result_model['SourceConnection'] = source
        result_model['TargetConnection'] = target
        result_model['Columns'] = columns
        return result_model

    @staticmethod
    def get_data_integration_models(data_integrations: List[DataIntegration]) -> List[DataIntegrationModel]:

        entities = []
        for data_integration in data_integrations:
            if data_integration.IsDeleted == 0:
                entity = DataIntegrationModels.get_data_integration_model(data_integration)
                entities.append(entity)
        return entities
