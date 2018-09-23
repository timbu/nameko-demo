from nameko.rpc import RpcProxy
from nameko.events import event_handler
from nameko_salesforce.streaming import handle_sobject_notification
from nameko_salesforce.api import SalesforceAPI

print("BASIC UP AND DOWN SYNC")


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
