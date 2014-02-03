from bson.json_util import dumps, loads
from event.mongo_event import trigger_add
from event.mongo_event import trigger_update
from event.mongo_event import trigger_delete
from abc import ABCMeta


def object_encoder(obj):
    if isinstance(obj, BaseModel):
        return obj.__dict__
    return obj


class BaseModel:
    ''' Base abstract class for models '''
    __metaclass__ = ABCMeta

    def save(self):
        '''
        Convert python object to acceptable mongodb JSON
        and call function for actual DB save
        '''
        trigger_add(loads(dumps(
            self.__dict__,
            default=object_encoder)),
            self.__class__.__dict__
        )

    def update(self):
        trigger_update(loads(dumps(
            self.__dict__,
            default=object_encoder)),
            self.__class__.__dict__
        )

    def delete(self):
        trigger_delete(loads(dumps(
            self.__dict__,
            default=object_encoder)),
            self.__class__.__dict__
        )


class Person(BaseModel):

    collection = 'peoples'
    db = 'people'

    def __init__(self, first, last, _id=None):
        self.first = first
        self.last = last
        if _id:
            self._id = _id


class PersonList(BaseModel):

    collection = 'persons'
    db = 'person'

    def __init__(self, *args, **kwargs):
        self.person_list = []

    def add(self, person):
        self.person_list.append(person)
