import json
from event.mongo_event import trigger_add
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
        trigger_add(json.loads(json.dumps(
            self.__dict__,
            default=object_encoder)),
            self.__class__.__dict__
        )

    def test(self):
        pass


class Person(BaseModel):

    collection = 'peoples'
    db = 'people'

    def __init__(self, first, last):
        self.first = first
        self.last = last


class PersonList(BaseModel):

    collection = 'persons'
    db = 'person'

    def __init__(self, *args, **kwargs):
        self.person_list = []

    def add(self, person):
        self.person_list.append(person)
