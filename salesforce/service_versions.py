"""
# BASIC UP AND DOWN SYNC
# SKIP DUPLICATES
# SOURCE TRACKING
# ASYNC TASKS
# DEBOUNCE
# RETRY
# TRACER
# SLACK

from nameko.rpc import RpcProxy
from nameko.events import event_handler

from nameko_salesforce.streaming import handle_sobject_notification
from nameko_salesforce.api import SalesforceAPI

from nameko_amqp_retry import entrypoint_retry
from nameko_slack.web import Slack
from nameko_tracer import Tracer

from platform_lock.dependencies.lock import DistributedLock

from source_tracker import SourceTracker
from tasks import ScheduleTask


def skip_duplicate_key(sobject_type, record_type, notification):
    return 'salesforce:skip_duplicate({})'.format(notification['event']['replayId'])


def debounce_key(payload):
    return 'salesforce:debounce'


class SalesforceService:

    name = 'salesforce'

    contacts_rpc = RpcProxy('contacts')

    salesforce = SalesforceAPI()

    lock = DistributedLock()

    source_tracker = SourceTracker()

    schedule_task = ScheduleTask()

    tracer = Tracer()

    slack = Slack()

    @event_handler('contacts', 'contact_created')
    def handle_platform_contact_created(self, payload):

        if self.source_tracker.is_sourced_from_salesforce():
            print("Ignoring event that was sourced from salesforce")
            return

        self.schedule_task(self.create_on_salesforce, payload)

    @handle_sobject_notification(
        'Contact', exclude_current_user=True,
        notify_for_operation_update=False
    )
    @lock.skip_duplicates(key=skip_duplicate_key)
    def handle_sf_contact_created(self, sobject_type, record_type, notification):
        self.schedule_task(self.create_on_platform, notification)

    @schedule_task.task
    @lock.debounce(key=debounce_key, repeat=True)
    @entrypoint_retry(
        retry_for=ValueError,
        limit=4,
        schedule=(1000, 1000, 2000),
    )
    def create_on_salesforce(self, payload):
        result = self.salesforce.Contact.create(
            {'LastName': payload['contact']['name']}
        )
        print('Created {} on salesforce'.format(result))
        self.slack.api_call(
            'chat.postMessage',
            channel='XYZ',
            text='Created contact {} on salesforce'.format(result['id']),
        )

    @schedule_task.task
    @lock.debounce(key=debounce_key, repeat=True)
    @entrypoint_retry(
        retry_for=ValueError,
        limit=4,
        schedule=(1000, 1000, 2000),
    )
    def create_on_platform(self, payload):
        with self.source_tracker.sourced_from_salesforce():
            contact = self.contacts_rpc.create_contact(
                {'name': payload['sobject']['Name']}
            )
        print('Created {} on platform'.format(contact))




# BASIC UP AND DOWN SYNC
# SKIP DUPLICATES
# SOURCE TRACKING
# ASYNC TASKS
# DEBOUNCE
# RETRY
# TRACER


from nameko.rpc import RpcProxy
from nameko.events import event_handler

from nameko_salesforce.streaming import handle_sobject_notification
from nameko_salesforce.api import SalesforceAPI

from nameko_amqp_retry import entrypoint_retry
from nameko_tracer import Tracer

from platform_lock.dependencies.lock import DistributedLock

from source_tracker import SourceTracker
from tasks import ScheduleTask


def skip_duplicate_key(sobject_type, record_type, notification):
    return 'salesforce:skip_duplicate({})'.format(notification['event']['replayId'])


def debounce_key(payload):
    return 'salesforce:debounce'


class SalesforceService:

    name = 'salesforce'

    contacts_rpc = RpcProxy('contacts')

    salesforce = SalesforceAPI()

    lock = DistributedLock()

    source_tracker = SourceTracker()

    schedule_task = ScheduleTask()

    tracer = Tracer()

    @event_handler('contacts', 'contact_created')
    def handle_platform_contact_created(self, payload):

        if self.source_tracker.is_sourced_from_salesforce():
            print("Ignoring event that was sourced from salesforce")
            return

        self.schedule_task(self.create_on_salesforce, payload)

    @handle_sobject_notification(
        'Contact', exclude_current_user=True,
        notify_for_operation_update=False
    )
    @lock.skip_duplicates(key=skip_duplicate_key)
    def handle_sf_contact_created(self, sobject_type, record_type, notification):
        self.schedule_task(self.create_on_platform, notification)

    @schedule_task.task
    @lock.debounce(key=debounce_key, repeat=True)
    @entrypoint_retry(
        retry_for=ValueError,
        limit=4,
        schedule=(1000, 1000, 2000),
    )
    def create_on_salesforce(self, payload):
        # print('Trying to create on salesforce...')
        # print("")
        # raise ValueError()

        result = self.salesforce.Contact.create(
            {'LastName': payload['contact']['name']}
        )
        print('Created {} on salesforce'.format(result))

    @schedule_task.task
    @lock.debounce(key=debounce_key, repeat=True)
    @entrypoint_retry(
        retry_for=ValueError,
        limit=4,
        schedule=(1000, 1000, 2000),
    )
    def create_on_platform(self, payload):
        with self.source_tracker.sourced_from_salesforce():
            contact = self.contacts_rpc.create_contact(
                {'name': payload['sobject']['Name']}
            )
        print('Created {} on platform'.format(contact))



# BASIC UP AND DOWN SYNC
# SKIP DUPLICATES
# SOURCE TRACKING
# ASYNC TASKS
# DEBOUNCE
# RETRY

from nameko.rpc import RpcProxy
from nameko.events import event_handler

from nameko_salesforce.streaming import handle_sobject_notification
from nameko_salesforce.api import SalesforceAPI

from nameko_amqp_retry import entrypoint_retry

from platform_lock.dependencies.lock import DistributedLock

from source_tracker import SourceTracker
from tasks import ScheduleTask


def skip_duplicate_key(sobject_type, record_type, notification):
    return 'salesforce:skip_duplicate({})'.format(notification['event']['replayId'])


def debounce_key(payload):
    return 'salesforce:debounce'


class SalesforceService:

    name = 'salesforce'

    contacts_rpc = RpcProxy('contacts')

    salesforce = SalesforceAPI()

    lock = DistributedLock()

    source_tracker = SourceTracker()

    schedule_task = ScheduleTask()

    @event_handler('contacts', 'contact_created')
    def handle_platform_contact_created(self, payload):

        if self.source_tracker.is_sourced_from_salesforce():
            print("Ignoring event that was sourced from salesforce")
            return

        self.schedule_task(self.create_on_salesforce, payload)

    @handle_sobject_notification(
        'Contact', exclude_current_user=True,
        notify_for_operation_update=False
    )
    @lock.skip_duplicates(key=skip_duplicate_key)
    def handle_sf_contact_created(self, sobject_type, record_type, notification):
        self.schedule_task(self.create_on_platform, notification)

    @schedule_task.task
    @lock.debounce(key=debounce_key, repeat=True)
    @entrypoint_retry(
        retry_for=ValueError,
        limit=4,
        schedule=(1000, 1000, 2000),
    )
    def create_on_salesforce(self, payload):
        print('Trying to create on salesforce...')
        print("")
        raise ValueError()

        result = self.salesforce.Contact.create(
            {'LastName': payload['contact']['name']}
        )
        print('Created {} on salesforce'.format(result))

    @schedule_task.task
    @lock.debounce(key=debounce_key, repeat=True)
    @entrypoint_retry(
        retry_for=ValueError,
        limit=4,
        schedule=(1000, 1000, 2000),
    )
    def create_on_platform(self, payload):
        with self.source_tracker.sourced_from_salesforce():
            contact = self.contacts_rpc.create_contact(
                {'name': payload['sobject']['Name']}
            )
        print('Created {} on platform'.format(contact))




# BASIC UP AND DOWN SYNC
# SKIP DUPLICATES
# SOURCE TRACKING
# ASYNC TASKS
# DEBOUNCE


from nameko.rpc import RpcProxy
from nameko.events import event_handler

from nameko_salesforce.streaming import handle_sobject_notification
from nameko_salesforce.api import SalesforceAPI

from platform_lock.dependencies.lock import DistributedLock

from source_tracker import SourceTracker
from tasks import ScheduleTask


def skip_duplicate_key(sobject_type, record_type, notification):
    return 'salesforce:skip_duplicate({})'.format(notification['event']['replayId'])


def debounce_key(payload):
    return 'salesforce:debounce'


class SalesforceService:

    name = 'salesforce'

    contacts_rpc = RpcProxy('contacts')

    salesforce = SalesforceAPI()

    lock = DistributedLock()

    source_tracker = SourceTracker()

    schedule_task = ScheduleTask()

    @event_handler('contacts', 'contact_created')
    def handle_platform_contact_created(self, payload):

        if self.source_tracker.is_sourced_from_salesforce():
            print("Ignoring event that was sourced from salesforce")
            return

        self.schedule_task(self.create_on_salesforce, payload)

    @handle_sobject_notification(
        'Contact', exclude_current_user=True,
        notify_for_operation_update=False
    )
    @lock.skip_duplicates(key=skip_duplicate_key)
    def handle_sf_contact_created(self, sobject_type, record_type, notification):
        self.schedule_task(self.create_on_platform, notification)

    @schedule_task.task
    @lock.debounce(key=debounce_key, repeat=True)
    def create_on_salesforce(self, payload):

        import eventlet
        eventlet.sleep(5)

        result = self.salesforce.Contact.create(
            {'LastName': payload['contact']['name']}
        )
        print('Created {} on salesforce'.format(result))

    @schedule_task.task
    @lock.debounce(key=debounce_key, repeat=True)
    def create_on_platform(self, payload):
        with self.source_tracker.sourced_from_salesforce():
            contact = self.contacts_rpc.create_contact(
                {'name': payload['sobject']['Name']}
            )
        print('Created {} on platform'.format(contact))





# BASIC UP AND DOWN SYNC
# SKIP DUPLICATES
# SOURCE TRACKING
# ASYNC TASKS

from nameko.rpc import RpcProxy
from nameko.events import event_handler

from nameko_salesforce.streaming import handle_sobject_notification
from nameko_salesforce.api import SalesforceAPI

from platform_lock.dependencies.lock import DistributedLock

from source_tracker import SourceTracker
from tasks import ScheduleTask


def skip_duplicate_key(sobject_type, record_type, notification):
    return 'salesforce:skip_duplicate({})'.format(notification['event']['replayId'])


class SalesforceService:

    name = 'salesforce'

    contacts_rpc = RpcProxy('contacts')

    salesforce = SalesforceAPI()

    lock = DistributedLock()

    source_tracker = SourceTracker()

    schedule_task = ScheduleTask()

    @event_handler('contacts', 'contact_created')
    def handle_platform_contact_created(self, payload):

        if self.source_tracker.is_sourced_from_salesforce():
            print("Ignoring event that was sourced from salesforce")
            return

        self.schedule_task(self.create_on_salesforce, payload)

    @handle_sobject_notification(
        'Contact', exclude_current_user=True,
        notify_for_operation_update=False
    )
    @lock.skip_duplicates(key=skip_duplicate_key)
    def handle_sf_contact_created(self, sobject_type, record_type, notification):
        self.schedule_task(self.create_on_platform, notification)

    @schedule_task.task
    def create_on_salesforce(self, payload):
        result = self.salesforce.Contact.create(
            {'LastName': payload['contact']['name']}
        )
        print('Created {} on salesforce'.format(result))

    @schedule_task.task
    def create_on_platform(self, payload):
        with self.source_tracker.sourced_from_salesforce():
            contact = self.contacts_rpc.create_contact(
                {'name': payload['sobject']['Name']}
            )
        print('Created {} on platform'.format(contact))




# BASIC UP AND DOWN SYNC
# SKIP DUPLICATES
# SOURCE TRACKING


from nameko.rpc import RpcProxy
from nameko.events import event_handler

from nameko_salesforce.streaming import handle_sobject_notification
from nameko_salesforce.api import SalesforceAPI

from platform_lock.dependencies.lock import DistributedLock

from source_tracker import SourceTracker


def skip_duplicate_key(sobject_type, record_type, notification):
    return 'salesforce:skip_duplicate({})'.format(notification['event']['replayId'])


class SalesforceService:

    name = 'salesforce'

    contacts_rpc = RpcProxy('contacts')

    salesforce = SalesforceAPI()

    lock = DistributedLock()

    source_tracker = SourceTracker()

    @event_handler('contacts', 'contact_created')
    def handle_platform_contact_created(self, payload):

        if self.source_tracker.is_sourced_from_salesforce():
            print("Ignoring event that was sourced from salesforce")
            return

        result = self.salesforce.Contact.create(
            {'LastName': payload['contact']['name']}
        )
        print('Created {} on salesforce'.format(result))

    @handle_sobject_notification(
        'Contact', exclude_current_user=True,
        notify_for_operation_update=False
    )
    @lock.skip_duplicates(key=skip_duplicate_key)
    def handle_sf_contact_created(self, sobject_type, record_type, notification):
        with self.source_tracker.sourced_from_salesforce():
            contact = self.contacts_rpc.create_contact(
                {'name': notification['sobject']['Name']}
            )
        print('Created {} on platform'.format(contact))



# BASIC UP AND DOWN SYNC
# SKIP DUPLICATES


from nameko.rpc import RpcProxy
from nameko.events import event_handler

from nameko_salesforce.streaming import handle_sobject_notification
from nameko_salesforce.api import SalesforceAPI

from platform_lock.dependencies.lock import DistributedLock


def skip_duplicate_key(sobject_type, record_type, notification):
    return 'salesforce:skip_duplicate({})'.format(notification['event']['replayId'])


class SalesforceService:

    name = 'salesforce'

    contacts_rpc = RpcProxy('contacts')

    salesforce = SalesforceAPI()

    lock = DistributedLock()

    @event_handler('contacts', 'contact_created')
    def handle_platform_contact_created(self, payload):
        result = self.salesforce.Contact.create(
            {'LastName': payload['contact']['name']}
        )
        print('Created {} on salesforce'.format(result))

    @handle_sobject_notification(
        'Contact', exclude_current_user=True,
        notify_for_operation_update=False
    )
    @lock.skip_duplicates(key=skip_duplicate_key)
    def handle_sf_contact_created(self, sobject_type, record_type, notification):
        contact = self.contacts_rpc.create_contact(
            {'name': notification['sobject']['Name']}
        )
        print('Created {} on platform'.format(contact))




# BASIC UP AND DOWN SYNC

from nameko.rpc import RpcProxy
from nameko.events import event_handler
from nameko_salesforce.streaming import handle_sobject_notification
from nameko_salesforce.api import SalesforceAPI


class SalesforceService:

    name = 'salesforce'

    contacts_rpc = RpcProxy('contacts')

    salesforce = SalesforceAPI()

    @event_handler('contacts', 'contact_created')
    def handle_platform_contact_created(self, payload):
        result = self.salesforce.Contact.create(
            {'LastName': payload['contact']['name']}
        )
        print('Created {} on salesforce'.format(result))

    @handle_sobject_notification(
        'Contact', exclude_current_user=True,
        notify_for_operation_update=False
    )
    def handle_sf_contact_created(self, sobject_type, record_type, notification):
        contact = self.contacts_rpc.create_contact(
            {'name': notification['sobject']['Name']}
        )
        print('Created {} on platform'.format(contact))
"""
