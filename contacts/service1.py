from nameko.rpc import rpc
from nameko.events import EventDispatcher

from nameko_sqlalchemy import Database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

print("BASIC SERVICE")


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
