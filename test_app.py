import unittest
import json
from app import app  

class ChampionAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test READ ALL 
    def test_get_all_champions(self):
        response = self.app.get('/champions')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('champions', data)

    # Test CREATE 
    def test_add_champion(self):
        new_champion = {
            "champion_name": "Teemo",
            "roleid": 2,
            "difficulty_level": "easy"
        }
        response = self.app.post('/champions', json=new_champion)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Champion added successfully")

    # Test READ ONE 
    def test_get_champion(self):
        response = self.app.get('/champions/1')  
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('champion_name', data)

    # Test UPDATE 
    def test_update_champion(self):
        update_data = {
            "champion_name": "Teemo Updated",
            "roleid": 2,
            "difficulty_level": "medium"
        }
        response = self.app.put('/champions/1', json=update_data)  
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Champion updated successfully")

    # Test DELETE 
    def test_delete_champion(self):
        champion_id = 1  
        response = self.app.delete(f'/champions/{champion_id}')
        
        
        self.assertIn(response.status_code, [200, 404, 400])
        
        if response.status_code == 400:
            data = json.loads(response.data)
            self.assertIn("cannot delete", data["error"].lower())

    # Test SEARCH JSON
    def test_search_champions(self):
        response = self.app.get('/champions/search?name=Teemo')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('champions', data)

        response = self.app.get('/champions/search?roleid=2')
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/champions/search?difficulty_level=easy')
        self.assertEqual(response.status_code, 200)

    # Test SEARCH XML
    def test_search_champions_xml(self):
        response = self.app.get('/champions/search?name=Teemo&format=xml')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<response>', response.data)  # XML root node is <response>

if __name__ == '__main__':
    unittest.main()
