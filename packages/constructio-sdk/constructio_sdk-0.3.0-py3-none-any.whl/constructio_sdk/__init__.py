from .compute import ComputeContext
from .prepare import PrepareContext


def init_compute(event):
    return ComputeContext(event['id'], event['uploadUrl'], event)


def init_prepare(event):
    return PrepareContext(event['id'], event)
