from functools import partial
from kombu import Exchange, Queue
from nameko.messaging import Publisher
from nameko_amqp_retry.messaging import consume


def task_routing_key(exchange_name, task_name):
    return '{}.task.{}'.format(exchange_name, task_name)


class ScheduleTaskWrapper:

    def __init__(self, publish_message, exchange_name):
        self.publish_message = publish_message
        self.exchange_name = exchange_name

    def __call__(self, entrypoint_method, payload):
        self.publish_message(
            payload,
            routing_key=task_routing_key(
                self.exchange_name, entrypoint_method.__name__
            )
        )


class ScheduleTask(Publisher):
    def __init__(self, exchange_name='demo-salesforce'):
        self.exchange_name = exchange_name
        self.exchange = Exchange(name=exchange_name)
        super().__init__(self.exchange)

    def get_dependency(self, worker_context):
        return ScheduleTaskWrapper(
            super().get_dependency(worker_context), self.exchange_name
        )

    def task(self, wrapped=None):
        """ Decorator to used define a schedulable task method
        """
        if wrapped is None:
            return partial(self.task)

        task_name = wrapped.__name__
        routing_key = task_routing_key(self.exchange_name, task_name)

        return consume(
            queue=Queue(
                exchange=self.exchange,
                routing_key=routing_key,
                name=routing_key,
            ),
        )(wrapped)
