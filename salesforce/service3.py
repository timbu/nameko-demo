from nameko.rpc import RpcProxy
from nameko.events import event_handler

from nameko_salesforce.streaming import handle_sobject_notification
from nameko_salesforce.api import SalesforceAPI

from platform_lock.dependencies.lock import DistributedLock

from source_tracker import SourceTracker


print("BASIC UP AND DOWN SYNC")
print("SOURCE TRACKING")
print("SKIP DUPLICATES")


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
