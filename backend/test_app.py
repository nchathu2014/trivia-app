import unittest
import json

from flask import Flask, jsonify, request, abort
from flask_migrate import Migrate
from models import setup_db, Plant, db, paginate_plants
from app import app


class PlantTestCase(unittest.TestCase):

        def setUp(self):
                """Executed before each test. Define test variables and initialize app."""
                self.app = app
                self.client = self.app.test_client
                self.database_name = "dbplants_test"
                self.database_path = database_path = "postgresql://{}:{}@{}/{}".format(
                    'postgres', '123', 'localhost', self.database_name)
                setup_db(self.app, self.database_path)

                self.new_plant = {
                        "name": "TEST PLANT",
                        "scientific_name": "TEST_SC_NAME",
                        "is_poisonous": True,
                        "primary_color": "TEST_PR_COLOR"
                }

        def tearDown(self):
                """reach after reach test"""
                pass

        def test_get_paginated_plants(self):
              res = self.client().get('/plants')
              data = json.loads(res.data)

              self.assertEqual(res.status_code, 200)
              self.assertEqual(data['success'], True)
              self.assertTrue(data['created'])
              self.assertTrue(len(data['plants']))
              self.assertTrue(data['total_plants'])

        def test_404_send_requesting_beyond_valid_page(self):
                res = self.client().get('/plants?page=1000') 
                data = json.loads(res.data)
                
                self.assertEqual(res.status_code,404)
                self.assertEqual(data['success'],False)
                self.assertEqual(data['message'],'resource not found')

        def test_update_plant_name(self):
               res = self.client().patch('/plants/4',json={'name':'test_name2'})
               data = json.loads(res.data)
               plant = Plant.query.filter(Plant.id =='4').one_or_none()
               
               self.assertEqual(res.status_code,200)
               self.assertEqual(data['success'],True)
               self.assertEqual(plant.format()['name'],'test_name2')

        def test_400_for_failed_update(self):
                res = self.client().patch('/plants/24',json=None)
                data = json.loads(res.data)
               
                #self.assertEqual(res.status_code,400)
                #self.assetEqual(data['success'],False)
                #self.assertEqual(data['message'],'bad request')
        
        def test_delete_book(self):
                res = self.client().delete('/plants/16')
                data = json.loads(res.data)

                plant = Plant.query.filter(Plant.id == '16').one_or_none()

                self.assertEqual(res.status_code,200)
                self.assertEqual(data['success'],True)
                self.assertTrue(data['total_plants'])
                self.assertTrue(data['deleted'])
                self.assertTrue(len(data['plants']))
                self.assertEqual(plant,None)
                

        def test_422_if_plant_doesnot_exists(self):
                res = self.client().delete('/plants/111')
                data = json.loads(res.data)

                self.assertEqual(res.status_code,422)
                self.assertEqual(data['success'],False)
                self.assertEqual(data['message'],'unprocessable')

        #POST

        def test_create_new_plant(self):
               res = self.client().post('/plants',json=self.new_plant)
               data = json.loads(res.data)
               
               self.assertEqual(res.status_code,200)
               self.assertEqual(data['success'],True)
               self.assertTrue(data['total_plants'])
              # self.assertTrue(data['created'])
               self.assertTrue(len(data['plants']))

        def test_405_method_not_allowed(self):
                res = self.client().post('/plants/10',json=self.new_plant)
                data = json.loads(res.data)
                
                self.assertEqual(res.status_code,405)
                self.assertEqual(data['success'],False)
                self.assertEqual(data['message'],'method not allowed')


if __name__ == "__main__":
    unittest.main()
