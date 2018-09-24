from functools import partial
from kombu import Exchange, Queue
from nameko.messaging import Publisher
from nameko_amqp_retry.messaging import consume


EXCHANGE = Exchange(name='demo-salesforce')


def task_routing_key(task_name):
    return 'demo-salesforce.task.{}'.format(task_name)


def task(wrapped=None):
    """ Decorator used define a schedulable task method
    """
    if wrapped is None:
        return partial(task)

    task_name = wrapped.__name__
    routing_key = task_routing_key(task_name)

    return consume(
        queue=Queue(
            exchange=EXCHANGE,
            routing_key=routing_key,
            name=routing_key,
        ),
    )(wrapped)


class ScheduleTaskWrapper:

    def __init__(self, publish_message):
        self.publish_message = publish_message

    def __call__(self, entrypoint_method, payload):
        self.publish_message(
            payload,
            routing_key=task_routing_key(entrypoint_method.__name__)
        )


class ScheduleTask(Publisher):
    """
    A DependencyProvider that allows you to schedule other marked entrypoints
    to be executed asynchronously.

    Implemented as a simple wrapper around the common publish/consume
    pattern.

    E.g. ::

        class MyService:

            schedule_task = ScheduleTask()

            @rpc
            def trigger(self):

                payload = {'x:': 1}
                self.schedule_task(self.do_work, payload)

                return 'scheduled'

            @task
            def do_work(self, payload):
                print(payload['x'])

    """

    def __init__(self):
        super().__init__(EXCHANGE)

    def get_dependency(self, worker_context):
        return ScheduleTaskWrapper(
            super().get_dependency(worker_context)
        )
