from nameko.events import EventDispatcher

from nameko_autocrud import AutoCrudWithEvents
from nameko_slack import rtm
from nameko_sqlalchemy import DatabaseSession


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


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

    @rtm.handle_message('^create contact (?P<name>\w+)')
    def slack_create_contact(self, event, message, name=None):
        return 'Contact created on platform: {}'.format(
            self.create_contact({'name': name})
        )

"""
# AUTOCRUD
# SLACK

from nameko.events import EventDispatcher

from nameko_autocrud import AutoCrudWithEvents
from nameko_slack import rtm
from nameko_sqlalchemy import DatabaseSession


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


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

    @rtm.handle_message('^create contact (?P<name>\w+)')
    def slack_create_contact(self, event, message, name=None):
        return 'Contact created on platform: {}'.format(
            self.create_contact({'name': name})
        )

"""

"""
# AUTOCRUD SERVICE

from nameko.events import EventDispatcher

from nameko_autocrud import AutoCrudWithEvents
from nameko_sqlalchemy import DatabaseSession

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


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


"""

"""
# BASIC SERVICE

from nameko.rpc import rpc
from nameko.events import EventDispatcher

from nameko_sqlalchemy import Database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


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

    db = Database(DeclarativeBase)
    dispatch = EventDispatcher()

    @rpc
    def get_contact(self, id_):
        with self.db.get_session() as session:
            contact = session.query(Contact).get(id_)
            return contact.to_dict()

    @rpc
    def create_contact(self, data):
        with self.db.get_session() as session:
            contact = Contact(**data)
            session.add(contact)

        self.dispatch('contact_created', {'contact': contact.to_dict()})

        return contact.to_dict()

"""
