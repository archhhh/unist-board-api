import unittest
from bson.objectid import ObjectId
from src.models.board import BoardModel
import conf
import json
import copy

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.collection = conf.client['test'].collection['boards']
        self.correctInput = {'_id': ObjectId(), 'icon': '😀', 'name': 'test', 'description': 'sup beach'}
        self.missingId = {'icon': '😀', 'name': 'test', 'description': 'sup beach'}
        self.missingIcon = {'_id': ObjectId(), 'name': 'test', 'description': 'sup beach'}
        self.missingName = {'_id': ObjectId(), 'icon': '😀', 'description': 'sup beach'}
        self.missingDescription = {'_id': ObjectId(), 'icon': '😀', 'name': 'test' }
        self.incorrectIdFormat = {'_id': 'qwq', 'icon': '😀', 'name': 'test', 'description': 'sup beach'}  
        self.incorrectIconFormat = {'_id': ObjectId(), 'icon': 524, 'name': 'test', 'description': 'sup beach'}
        self.incorrectNameFormat = { '_id': ObjectId(), 'icon': '😀', 'name': False,  'description': 'sup beach' }
        self.incorrectDescriptionFormat = {'_id': ObjectId(), 'icon': '😀', 'name': 'test', 'description': 1231251}
        self.emptyIcon = {'_id': ObjectId(), 'icon': '', 'name': 'test', 'description': 'sup beach'}
        self.emptyName = {'_id': ObjectId(), 'icon': '😀', 'name': '', 'description': 'sup beach'}
        self.emptyDescription = {'_id': ObjectId(), 'icon': '😀', 'name': 'test', 'description': ''}
    
    def test_board_input_validate(self):
        self.assertEqual(BoardModel.validate(self.correctInput), 0)
        self.assertEqual(BoardModel.validate(self.missingId), 'Missing parameter')
        self.assertEqual(BoardModel.validate(self.missingIcon), 'Missing parameter')
        self.assertEqual(BoardModel.validate(self.missingName), 'Missing parameter')
        self.assertEqual(BoardModel.validate(self.missingDescription), 'Missing parameter')
        self.assertEqual(BoardModel.validate(self.incorrectIdFormat), '_id Not an instance of ObjectId')
        self.assertEqual(BoardModel.validate(self.incorrectIconFormat), 'icon Not an instance of string')
        self.assertEqual(BoardModel.validate(self.incorrectNameFormat), 'name Not an instance of string')
        self.assertEqual(BoardModel.validate(self.incorrectDescriptionFormat), 'description Not an instance of string')
        self.assertEqual(BoardModel.validate(self.emptyIcon), 'icon is empty')
        self.assertEqual(BoardModel.validate(self.emptyName), 'name is empty')
        self.assertEqual(BoardModel.validate(self.emptyDescription), 'description is empty')

    @unittest.expectedFailure
    def test_init_fail(self):
        board = BoardModel(self.missingId)
        self.assertEqual(1, 0, "broken")

    def test_init(self):
        board = BoardModel(self.correctInput)
        self.assertEqual(board._id, self.correctInput['_id'])
        self.assertEqual(board.name, self.correctInput['name'])
        self.assertEqual(board.icon, self.correctInput['icon'])
        self.assertEqual(board.description, self.correctInput['description'])

    @unittest.expectedFailure
    def test_set_values_fail(self):
        board = BoardModel(self.correctInput)
        board.set_values(self.missingIcon)
        self.assertEqual(1, 0, "broken")

    def test_set_values(self):
        board = BoardModel(self.correctInput)
        inp = {'_id': self.correctInput['_id'], 'icon': '😀', 'name': 'test', 'description': 'sup beach'}
        board.set_values(inp)
        self.assertEqual(board._id, inp['_id'])
        self.assertEqual(board.name, inp['name'])
        self.assertEqual(board.icon, inp['icon'])
        self.assertEqual(board.description, inp['description'])

    def test_init_good(self):
        board = BoardModel(self.correctInput)
        self.assertEqual(board._id == self.correctInput['_id'] and board.name == self.correctInput['name'] and board.icon == self.correctInput['icon'] and board.description == self.correctInput['description'], True)

    def test_insert_and_find(self):
        self.collection.drop()
        board = BoardModel(self.correctInput)
        self.assertNotEqual(board.insert_one(), -1)
        board = BoardModel.find_one(self.correctInput)
        self.assertNotEqual(board, None)
        self.assertEqual(board._id, self.correctInput['_id'])
        self.assertEqual(board.name, self.correctInput['name'])
        self.assertEqual(board.icon, self.correctInput['icon'])
        self.assertEqual(board.description, self.correctInput['description'])
    
    def test_insert_existing(self):
        self.collection.drop()
        board = BoardModel(self.correctInput)
        self.assertNotEqual(board.insert_one(), -1)
        self.assertEqual(board.insert_one(), -1)

    def test_to_json(self):
        board = BoardModel(self.correctInput)
        board_JSONed = board.to_json()
        board_dict = json.loads(board_JSONed)
        self.assertEqual(len(board_dict), 4)
        self.assertEqual(str(board._id), board_dict['_id'])
        self.assertEqual(board.icon, board_dict['icon'])
        self.assertEqual(board.name, board_dict['name'])
        self.assertEqual(board.description, board_dict['description'])

    def test_insert_many(self):
        self.collection.drop()
        correctInput = [
            {'_id': ObjectId(), 'icon': '😀', 'name': 'test0', 'description': 'sup beach0'},
            {'_id': ObjectId(), 'icon': '😃', 'name': 'test1', 'description': 'sup beach1'},
            {'_id': ObjectId(), 'icon': '😄', 'name': 'test2', 'description': 'sup beach2'}
        ]
        boards = [BoardModel(inp) for inp in correctInput]
        self.assertNotEqual(BoardModel.insert_many(boards), -1)
        for inp in correctInput:
            board = BoardModel.find_one(inp)
            self.assertNotEqual(board, None)
            self.assertEqual(board._id, inp['_id'])
            self.assertEqual(board.icon, inp['icon'])
            self.assertEqual(board.name, inp['name'])
            self.assertEqual(board.description, inp['description'])

    def test_insert_existing_many(self):
        self.collection.drop()
        correctInput = [
            {'_id': ObjectId(), 'icon': '😀', 'name': 'test0', 'description': 'sup beach0'},
            {'_id': ObjectId(), 'icon': '😃', 'name': 'test1', 'description': 'sup beach1'},
            {'_id': ObjectId(), 'icon': '😄', 'name': 'test2', 'description': 'sup beach2'}
        ]
        boards = [BoardModel(inp) for inp in correctInput]
        self.assertNotEqual(BoardModel.insert_many(boards), -1)
        self.assertEqual(boards[0].insert_one(), -1)
        self.assertEqual(boards[1].insert_one(), -1)
        self.assertEqual(boards[2].insert_one(), -1)

    def test_update(self):
        self.collection.drop()
        board = BoardModel(self.correctInput)
        board.insert_one()
        old_board = BoardModel.find_one({'_id': self.correctInput['_id']})
        newInput = copy.deepcopy(self.correctInput)
        newInput['name'] = 'newtest'
        board.set_values(newInput)
        board.update_one()
        new_board = BoardModel.find_one({'_id': newInput['_id']})
        self.assertNotEqual(new_board, None)
        self.assertEqual(new_board._id, old_board._id)
        self.assertEqual(new_board.name, newInput['name'])

    def test_delete(self):
        self.collection.drop()
        board = BoardModel(self.correctInput)
        board.insert_one()
        self.assertEqual(board.delete(), 0)
        self.assertEqual(BoardModel.find_one({'_id': board._id}), None)

if __name__ == '__main__':
    unittest.main()