from contextlib import contextmanager

from nameko.extensions import DependencyProvider


SALESFORCE_SOURCE_CONTEXT_KEY = 'sourced_from_salesforce'


class _Tracker:

    def __init__(self, worker_ctx):
        self.worker_ctx = worker_ctx

    @contextmanager
    def sourced_from_salesforce(self):
        self.worker_ctx.data[SALESFORCE_SOURCE_CONTEXT_KEY] = True
        yield
        self.worker_ctx.data.pop(SALESFORCE_SOURCE_CONTEXT_KEY, None)

    def is_sourced_from_salesforce(self):
        return self.worker_ctx.data.get(SALESFORCE_SOURCE_CONTEXT_KEY) or False


class SourceTracker(DependencyProvider):
    def get_dependency(self, worker_ctx):
        return _Tracker(worker_ctx)
