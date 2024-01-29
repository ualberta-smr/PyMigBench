import json
from datetime import datetime, timedelta
from typing import List

from flask_restx import fields

from controllers.common.models.CommonModels import EntityModel, CommonModels
from controllers.job.models.JobModels import JobModels
from controllers.operation.models.DataOperationModels import DataOperationModels
from IocManager import IocManager
from models.dao.operation import DataOperationJob


class DataOperationJobModel(EntityModel):
    def __init__(self,
                 Id: int = None,
                 StartDate: datetime = None,
                 EndDate: datetime = None,
                 Cron: str = None,
                 DataOperationId: int = None,
                 ApSchedulerJobId: int = None,
                 DataIntegration=None,
                 ApSchedulerJob=None,
                 IsDeleted=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id: int = Id
        self.StartDate: datetime = StartDate
        self.EndDate: datetime = EndDate
        self.Cron: int = Cron
        self.DataOperationId: int = DataOperationId
        self.ApSchedulerJobId: int = ApSchedulerJobId
        self.DataIntegration = DataIntegration
        self.ApSchedulerJob = ApSchedulerJob
        self.IsDeleted = IsDeleted


class JobSchedulerModels:
    ns = IocManager.api.namespace('JobScheduler', description='Job Scheduler endpoints',
                                  path='/api/JobScheduler')

    start_operation_model = IocManager.api.model('Schedule', {
        'OperationName': fields.String(description='Operation name', required=True),
        'RunDate': fields.DateTime(
            description="Job run date.", required=True,
            example=(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'))
    })

    start_operation_with_cron_model = IocManager.api.model('ScheduleDataOperation', {
        'OperationName': fields.String(description='Data Operation Name', required=True),
        'Cron': fields.String(description="Job cron value. ", required=True, example='*/1 * * * *'),
        'StartDate': fields.DateTime(
            description="Job start date. The start date for the job can be entered if necessary.", required=False,
            example=(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')),
        'EndDate': fields.DateTime(
            description="Job End date. The end date for the job can be entered if necessary.", required=False,
            example=(datetime.now() + timedelta(seconds=10)).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'),
    })
    delete_operation_job_model = IocManager.api.model('DeleteOperationJob', {
        'DataOperationJobId': fields.Integer(description='DataOperationJobId', required=True)
    })
    delete_operation_cron_job_model = IocManager.api.model('DeleteOperationCronJob', {
        'DataOperationName': fields.String(description='Data Operation Name', required=True)
    })

    @staticmethod
    def get_data_operation_job_model(data_operation_job: DataOperationJob) -> DataOperationJobModel:
        entity_model = DataOperationJobModel(
            Id=data_operation_job.Id,
            Cron=data_operation_job.Cron,
            StartDate=data_operation_job.StartDate,
            EndDate=data_operation_job.EndDate,
            DataOperationId=data_operation_job.DataOperationId,
            ApSchedulerJobId=data_operation_job.ApSchedulerJobId,
            IsDeleted=data_operation_job.IsDeleted,
        )
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        result_model['DataOperation'] = DataOperationModels.get_data_operation_result_model(
            data_operation_job.DataOperation)
        result_model['ApSchedulerJob'] = JobModels.get_ap_scheduler_job_model(
            data_operation_job.ApSchedulerJob)
        return result_model

    @staticmethod
    def get_data_operation_job_models(data_operation_jobs: List[DataOperationJob]) -> List[
        DataOperationJobModel]:
        entities = []
        for data_operation_job in data_operation_jobs:
            entity = JobSchedulerModels.get_data_operation_job_model(data_operation_jobs)
            entities.append(entity)
        return entities
