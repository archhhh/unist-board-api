
from pymongo import MongoClient
import json
from bson.objectid import ObjectId
import conf

collection = conf.client['test'].collection['boards']

class BoardModel:

    _id = ""
    icon = ""
    name = ""
    description = ""

    @staticmethod
    def find_one(query):
        board = collection.find_one(query)
        if board == None:
            return None
        return BoardModel(board)

    @staticmethod
    def insert_many(boards):
        for board in boards:
            if BoardModel.find_one(board.__dict__):
                return -1
        collection.insert_many([board.__dict__ for board in boards])
        return boards

    @staticmethod
    def validate(params):
        if '_id' not in params or 'icon' not in params or 'name' not in params or 'description' not in params:
            return 'Missing parameter'
        if not isinstance(params['_id'], ObjectId):
            return '_id Not an instance of ObjectId'
        if not isinstance(params['icon'], str):
            return 'icon Not an instance of string'
        if len(params['icon']) == 0:
            return 'icon is empty'
        if not isinstance(params['name'], str):
            return 'name Not an instance of string'
        if len(params['name']) == 0:
            return 'name is empty'
        if not isinstance(params['description'], str):
            return 'description Not an instance of string'
        if len(params['description']) == 0:
            return 'description is empty'
        return 0

    def __init__(self, params):
        self.set_values(params)

    def insert_one(self):
        board = BoardModel.find_one({'$or': [ { '_id': self._id }, { 'icon': self.icon }, { 'name': self.name }, { 'description': self.description } ]})
        if board == None:
            return collection.insert_one(self.__dict__).inserted_id
        return -1

    def update_one(self):
        if BoardModel.find_one({'_id': self._id }) != None:
            collection.update_one({'_id': self._id}, {'$set': self.__dict__})
            return self._id
        return -1

    def delete(self):
        if BoardModel.find_one({'_id': self._id }) != None:
            collection.delete_one({'_id': self._id})
            return 0
        return -1

    def set_values(self, new_values):
        res = BoardModel.validate(new_values)
        if res != 0:
            raise Exception(res)
        self._id = new_values['_id']
        self.icon = new_values['icon']
        self.name = new_values['name']
        self.description = new_values['description']

    def to_json(self):
        return json.dumps(self.__dict__, default=str)