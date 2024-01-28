import json
from typing import List

from flask_restx import fields

from controllers.common.models.CommonModels import EntityModel, CommonModels
from IocManager import IocManager
from models.dao.aps.ApSchedulerJob import ApSchedulerJob
from models.dao.aps.ApSchedulerJobEvent import ApSchedulerJobEvent


class ApSchedulerJobModel(EntityModel):
    __tablename__ = "ApSchedulerJob"

    def __init__(self,
                 JobId=None,
                 NextRunTime=None,
                 FuncRef=None,
                 IsDeleted=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.JobId = JobId
        self.NextRunTime = NextRunTime
        self.FuncRef = FuncRef
        self.IsDeleted = IsDeleted


class ApSchedulerJobEventModel():
    def __init__(self,
                 JobId=None,
                 EventId=None,
                 EventName=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.JobId = JobId
        self.EventId = EventId
        self.EventName = EventName


class JobModels:
    ns = IocManager.api.namespace('Job', description='Job scheduler endpoints', path='/api/Job')

    RemoveJobModel = IocManager.api.model('RemoveJob', {
        'JobId': fields.Integer(description='', required=True),
    })

    @staticmethod
    def get_ap_scheduler_job_model(ap_scheduler_job: ApSchedulerJob) -> ApSchedulerJobModel:
        result = ApSchedulerJobModel(
            JobId=ap_scheduler_job.JobId,
            NextRunTime=ap_scheduler_job.NextRunTime,
            FuncRef=ap_scheduler_job.FuncRef,
            Id=ap_scheduler_job.Id,
            IsDeleted=ap_scheduler_job.IsDeleted,
        )
        entity = json.loads(json.dumps(result.__dict__, default=CommonModels.date_converter))
        return entity

    @staticmethod
    def get_ap_scheduler_job_models(ap_scheduler_jobs: List[ApSchedulerJob]) -> List[ApSchedulerJobModel]:
        entities = []
        for ap_scheduler_job in ap_scheduler_jobs:
            entity = JobModels.get_ap_scheduler_job_model(ap_scheduler_job)
            entities.append(entity)
        return entities

    @staticmethod
    def get_ap_scheduler_job_events_model(ap_scheduler_job_events: List[ApSchedulerJobEvent]) -> List[
        ApSchedulerJobEventModel]:
        entities = []
        for ap_scheduler_job_event in ap_scheduler_job_events:
            result = ApSchedulerJobEventModel(
                JobId=ap_scheduler_job_event.ApSchedulerJobId,
                EventId=ap_scheduler_job_event.EventId,
                EventName=ap_scheduler_job_event.ApSchedulerEvent.Name,
            )
            entity = json.loads(json.dumps(result.__dict__, default=CommonModels.date_converter))
            entities.append(entity)
        return entities
