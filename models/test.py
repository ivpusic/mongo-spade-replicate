from event.mongo_event import trigger_add
import json
from json import JSONEncoder
from bson import json_util
from bson.json_util import dumps

def object_encoder(obj):
    if isinstance(obj, BaseModel):
        return obj.__dict__
    return obj

class BaseModel:

    def save(self):
        if 'db' not in self.__dict__:
            self.db = 'default'
        if 'collection' not in self.__dict__:
            self.collection = 'default'
        trigger_add(json.loads(json.dumps(self.__dict__, default=object_encoder)))

    def set_db(self, db):
        self.db = db

    def set_collection(self, collection):
        self.collection = collection

class Person(BaseModel):

    def __init__(self, first, last):
        self.first= first
        self.last = last

class PersonList(BaseModel):

    def __init__(self, *args, **kwargs):
        self.person_list = []

    def add(self, person):
        self.person_list.append(person)
