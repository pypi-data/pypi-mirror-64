from enum import Enum
from typing import List, TypedDict


class JobType(Enum):
    REVIEWS = "reviews"
    STATUSES = "statuses"


class Args(TypedDict):
    ...


class ReviewsArgs(Args):
    user_id: str
    url: str


class StatusesArgs(Args):
    user_id: str
    biz_id: str
    review_id: str


class DispatcherJob(TypedDict):
    job_type: JobType
    args_list: List[Args]


class WorkerJob(TypedDict):
    job_type: JobType
    args: Args


class WorkerResult(TypedDict):
    job_type: JobType
    result: TypedDict
