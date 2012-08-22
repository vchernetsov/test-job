from django.test import TestCase
from django.test.client import Client
import json
c = Client()



class SimpleTest(TestCase):


    def test_index(self):
        response = c.get('/testapp/')
        self.assertEqual(response.status_code, 200)


    def test_add_entry(self):
        response = c.post('/table_add_ajax/rooms/', {"department": "test_room_entry", "spots": 10})
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIsInstance(content, dict)
        self.assertIsInstance(content['id'], int)
        self.asserGreater(content['id'], 0)
        return content

        
    def test_table_fetch(self):
        response = c.get('/table_ajax/rooms/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.content), list)


    def table_struct_fetch(self):
        response = c.get('/table_struct_ajax/')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIsInstance(content, dict)


    def test_add_entry(self):
        response = c.post('/table_add_ajax/rooms/', {"department": "test_room_entry", "spots": 10})
        new_entry = json.loads(response.content)

        response = c.post('/table_update_ajax/rooms-%s-department/' % new_entry['id'], {"value": "test_room_entry_updated"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '1')

