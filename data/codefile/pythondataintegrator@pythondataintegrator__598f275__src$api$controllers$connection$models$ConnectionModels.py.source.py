import json
from typing import List

from flask_restplus import fields

from controllers.common.models.CommonModels import EntityModel, CommonModels
from IocManager import IocManager
from models.dao.connection import ConnectionFile, ConnectionServer, ConnectionQueue
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionDatabase import ConnectionDatabase
from models.dao.connection.ConnectorType import ConnectorType
from models.dao.connection.ConnectionType import ConnectionType


class ConnectionTypeModel(EntityModel):

    def __init__(self,
                 Id=None,
                 Name=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id = Id
        self.Name = Name


class ConnectorTypeModel(EntityModel):

    def __init__(self,
                 Id=None,
                 Name=None,
                 ConnectionType=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id = Id
        self.Name = Name
        self.ConnectionType = ConnectionType


class ConnectionModel(EntityModel):
    def __init__(self,
                 Id=None,
                 Name=None,
                 ConnectionType=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id = Id
        self.Name = Name
        self.ConnectionType = ConnectionType


class ConnectionServerModel(EntityModel):

    def __init__(self,
                 Id=None,
                 Host=None,
                 Port=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id = Id
        self.Host = Host
        self.Port = Port


class ConnectionDatabaseModel(EntityModel):

    def __init__(self,
                 Id=None,
                 Sid: str = None,
                 ServiceName: str = None,
                 DatabaseName: str = None,
                 User: str = None,
                 Password: str = None,
                 Connection=None,
                 ConnectorType=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id = Id
        self.Sid: str = Sid
        self.ServiceName: str = ServiceName
        self.DatabaseName: str = DatabaseName
        self.User: str = User
        self.Password: str = Password
        self.Connection = Connection
        self.ConnectorType = ConnectorType


class ConnectionFileModel(EntityModel):

    def __init__(self,
                 Id=None,
                 User: str = None,
                 Password: str = None,
                 Connection=None,
                 ConnectorType=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id = Id
        self.User: str = User
        self.Password: str = Password
        self.Connection = Connection
        self.ConnectorType = ConnectorType


class ConnectionQueueModel(EntityModel):

    def __init__(self,
                 Id=None,
                 Protocol: str = None,
                 Mechanism: str = None,
                 User: str = None,
                 Password: str = None,
                 Connection=None,
                 ConnectorType=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id = Id
        self.Protocol: str = Protocol
        self.Mechanism: str = Mechanism
        self.User: str = User
        self.Password: str = Password
        self.Connection = Connection
        self.ConnectorType = ConnectorType


class ConnectionModels:
    ns = IocManager.api.namespace('Connection', description='Connection endpoints', path='/api/Connection')

    create_connection_database_model = IocManager.api.model('ConnectionDatabaseModel', {
        'Name': fields.String(description='Operation code value', required=True),
        'ConnectorTypeName': fields.String(description='ConnectorTypeName', required=True),
        'Host': fields.String(description='Host'),
        'Port': fields.Integer(description='Port'),
        'Sid': fields.String(description='Sid'),
        'ServiceName': fields.String(description='ServiceName'),
        'DatabaseName': fields.String(description='DatabaseName'),
        'User': fields.String(description='User'),
        'Password': fields.String(description='Password'),
    })

    create_connection_file_model = IocManager.api.model('ConnectionFileModel', {
        'Name': fields.String(description='Operation code value', required=True),
        'ConnectorTypeName': fields.String(description='ConnectorTypeName', required=True),
        'Host': fields.String(description='Host'),
        'Port': fields.Integer(description='Port'),
        'User': fields.String(description='User'),
        'Password': fields.String(description='Password'),
    })
    create_connection_server_model = IocManager.api.model('ConnectionServerModel', {
        'Host': fields.String(description='Host'),
        'Port': fields.Integer(description='Port'),
    })
    create_connection_queue_model = IocManager.api.model('ConnectionQueueModel', {
        'Name': fields.String(description='Operation code value', required=True),
        'ConnectorTypeName': fields.String(description='ConnectorTypeName', required=True),
        'Servers': fields.List(fields.Nested(create_connection_server_model), description='Queue Servers',
                               required=False),
        'Protocol': fields.String(description='Protocol'),
        'Mechanism': fields.String(description='Mechanism'),
        'User': fields.String(description='User'),
        'Password': fields.String(description='Password'),
    })

    delete_connection_database_model = IocManager.api.model('DeleteConnectionDatabaseModel', {
        'Id': fields.Integer(description='Connection Database Id', required=True),
    })

    check_connection_database_model = IocManager.api.model('CheckConnectionDatabaseModel', {
        'Name': fields.String(description='Connection Name', required=True),
        'Schema': fields.String(description='Schema For Check Connection', required=False, example=""),
        'Table': fields.String(description='Table For Check Connection', required=False, example=""),
    })

    @staticmethod
    def get_connection_server_model(connection_server: ConnectionServer) -> ConnectionServerModel:
        entity_model = ConnectionServerModel(
            Id=connection_server.Id,
            Host=connection_server.Host,
            Port=connection_server.Port,
        )
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        return result_model

    @staticmethod
    def get_connection_server_models(connection_servers: List[ConnectionServer]) -> List[ConnectionServerModel]:

        entities = []
        for connection_server in connection_servers:
            if connection_server.IsDeleted == 0:
                entity = ConnectionModels.get_connection_server_model(connection_server)
                entities.append(entity)
        return entities

    @staticmethod
    def get_connection_type_model(connection_type: ConnectionType) -> ConnectionTypeModel:
        entity_model = ConnectionTypeModel(
            Id=connection_type.Id,
            Name=connection_type.Name,
        )
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        return result_model

    @staticmethod
    def get_connection_type_models(connection_types: List[ConnectionType]) -> List[ConnectionTypeModel]:

        entities = []
        for connection_type in connection_types:
            entity = ConnectionModels.get_connection_type_model(connection_type)
            entities.append(entity)
        return entities

    @staticmethod
    def get_connector_type_model(connector_type: ConnectorType) -> ConnectorTypeModel:
        connection_type = ConnectionModels.get_connection_type_model(connector_type.ConnectionType)
        entity_model = ConnectorTypeModel(
            Id=connector_type.Id,
            Name=connector_type.Name,
        )
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        result_model['ConnectionType'] = connection_type

        return result_model

    @staticmethod
    def get_connector_type_models(connector_types: List[ConnectorType]) -> List[ConnectorTypeModel]:

        entities = []
        for connector_type in connector_types:
            entity = ConnectionModels.get_connector_type_model(connector_type)
            entities.append(entity)
        return entities

    @staticmethod
    def get_connection_model(connection: Connection) -> ConnectionModel:
        connection_type = ConnectionModels.get_connection_type_model(connection.ConnectionType)
        entity_model = ConnectionModel(
            Id=connection.Id,
            Name=connection.Name,
        )
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        result_model['ConnectionType'] = connection_type
        return result_model

    @staticmethod
    def get_connection_database_entity_model(connection_database: ConnectionDatabase) -> ConnectionDatabaseModel:
        entity_model = ConnectionDatabaseModel(
            Id=connection_database.Id,
            Sid=connection_database.Sid,
            ServiceName=connection_database.ServiceName,
            DatabaseName=connection_database.DatabaseName,
            User='***',  # connection_database.User
            Password='***'  # connection_database.Password
        )
        return entity_model

    @staticmethod
    def get_connection_file_entity_model(connection_file: ConnectionFile) -> ConnectionFileModel:
        entity_model = ConnectionFileModel(
            Id=connection_file.Id,
            User='***',  # connection_database.User
            Password='***'  # connection_database.Password
        )
        return entity_model

    @staticmethod
    def get_connection_queue_entity_model(connection_queue: ConnectionQueue) -> ConnectionQueueModel:
        entity_model = ConnectionQueueModel(
            Id=connection_queue.Id,
            Protocol=connection_queue.Protocol,
            Mechanism=connection_queue.Mechanism,
            User='***',  # connection_database.User
            Password='***'  # connection_database.Password
        )
        return entity_model

    @staticmethod
    def get_connection_database_model(connection_database: ConnectionDatabase) -> ConnectionDatabaseModel:
        connection = ConnectionModels.get_connection_model(connection_database.Connection)
        connector_type = ConnectionModels.get_connector_type_model(connection_database.ConnectorType)
        entity_model = ConnectionModels.get_connection_database_entity_model(connection_database)
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        result_model['ConnectorType'] = connector_type
        result_model['Connection'] = connection
        return result_model

    @staticmethod
    def get_connection_file_model(connection_file: ConnectionFile) -> ConnectionFileModel:
        connection = ConnectionModels.get_connection_model(connection_file.Connection)
        connector_type = ConnectionModels.get_connector_type_model(connection_file.ConnectorType)
        entity_model = ConnectionModels.get_connection_file_entity_model(connection_file)
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        result_model['ConnectorType'] = connector_type
        result_model['Connection'] = connection
        return result_model

    @staticmethod
    def get_connection_database_models(connection_databases: List[ConnectionDatabase]) -> List[ConnectionDatabaseModel]:

        entities = []
        for connection_database in connection_databases:
            entity = ConnectionModels.get_connection_database_model(connection_database)
            entities.append(entity)
        return entities

    @staticmethod
    def get_connection_database_result_model(connection_database: ConnectionDatabase) -> ConnectionDatabaseModel:
        connector_type = ConnectionModels.get_connector_type_model(connection_database.ConnectorType)
        entity_model = ConnectionModels.get_connection_database_entity_model(connection_database)
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        result_model['ConnectorType'] = connector_type
        return result_model

    @staticmethod
    def get_connection_file_result_model(connection_file: ConnectionFile) -> ConnectionFileModel:
        connector_type = ConnectionModels.get_connector_type_model(connection_file.ConnectorType)
        entity_model = ConnectionModels.get_connection_file_entity_model(connection_file)
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        result_model['ConnectorType'] = connector_type
        return result_model

    @staticmethod
    def get_connection_queue_result_model(connection_queue: ConnectionQueue) -> ConnectionQueueModel:
        connector_type = ConnectionModels.get_connector_type_model(connection_queue.ConnectorType)
        entity_model = ConnectionModels.get_connection_queue_entity_model(connection_queue)
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        result_model['ConnectorType'] = connector_type
        return result_model

    @staticmethod
    def get_connection_result_model(connection: Connection) -> ConnectionModel:
        connection_type = ConnectionModels.get_connection_type_model(connection.ConnectionType)
        entity_model = ConnectionModel(
            Id=connection.Id,
            Name=connection.Name,
        )
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        result_model['ConnectionType'] = connection_type
        if connection.ConnectionServers is not None:
            result_model['Servers'] = ConnectionModels.get_connection_server_models(connection.ConnectionServers)

        if connection.Database is not None:
            connection_database = ConnectionModels.get_connection_database_result_model(connection.Database)
            result_model['Database'] = connection_database
        if connection.File is not None:
            connection_file = ConnectionModels.get_connection_file_result_model(connection.File)
            result_model['File'] = connection_file
        if connection.Queue is not None:
            connection_queue = ConnectionModels.get_connection_queue_result_model(connection.Queue)
            result_model['Queue'] = connection_queue
        return result_model

    @staticmethod
    def get_connection_result_models(connections: List[Connection]) -> List[ConnectionModel]:
        entities = []
        for connection in connections:
            entity = ConnectionModels.get_connection_result_model(connection)
            entities.append(entity)
        return entities
