

from nameko.events import EventDispatcher

from nameko_autocrud import AutoCrudWithEvents
from nameko_sqlalchemy import DatabaseSession

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

print("BASIC SERVICE")
print("AUTOCRUD")


class ModelBase:
    pass


DeclarativeBase = declarative_base(cls=ModelBase)


class Contact(DeclarativeBase):

    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name}


class ContactsService:

    name = 'contacts'

    session = DatabaseSession(DeclarativeBase)
    dispatch = EventDispatcher()

    auto_crud = AutoCrudWithEvents(
        session, dispatch, 'contact',
        model_cls=Contact,
        get_method_name='get_contact',
        create_method_name='create_contact',
        update_method_name='update_contact',
        list_method_name='list_contacts',
        count_method_name='count_contacts',
        create_event_name='contact_created',
        update_event_name='contact_updated',
    )
