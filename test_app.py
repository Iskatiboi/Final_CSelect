import unittest
import json
from app import app  

class ChampionAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # LOGIN to get JWT token
        login_response = self.app.post(
            '/login',
            json={
                "username": "admin",
                "password": "admin123"
            }
        )

        data = json.loads(login_response.data)
        self.token = data['access_token']

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    # READ ALL 
    def test_get_all_champions(self):
        response = self.app.get('/champions')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('champions', data)

    #  CREATE 
    def test_add_champion(self):
        new_champion = {
            "champion_name": "Teemo",
            "roleid": 2,
            "difficulty_level": "easy"
        }

        response = self.app.post(
            '/champions',
            json=new_champion,
            headers=self.headers
        )

        self.assertEqual(response.status_code, 201)

    #  READ ONE 
    def test_get_champion(self):
        response = self.app.get('/champions/1')
        self.assertIn(response.status_code, [200, 404])

    #  UPDATE 
    def test_update_champion(self):
        update_data = {
            "champion_name": "Teemo Updated",
            "roleid": 2,
            "difficulty_level": "medium"
        }

        response = self.app.put(
            '/champions/1',
            json=update_data,
            headers=self.headers
        )

        self.assertIn(response.status_code, [200, 404])

    #  DELETE 
    def test_delete_champion(self):
        response = self.app.delete(
            '/champions/1',
            headers=self.headers
        )

        self.assertIn(response.status_code, [200, 404, 400])

        if response.status_code == 400:
            data = json.loads(response.data)
            self.assertIn("cannot delete", data["error"].lower())

    #  SEARCH JSON 
    def test_search_champions(self):
        response = self.app.get('/champions/search?name=Teemo')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIn('champions', data)

        response = self.app.get('/champions/search?roleid=2')
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/champions/search?difficulty_level=easy')
        self.assertEqual(response.status_code, 200)

    #  SEARCH XML 
    
    def test_search_champions_xml(self):
        response = self.app.get('/champions/search?name=Teemo&format=xml')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<champions>', response.data)


if __name__ == '__main__':
    unittest.main()
