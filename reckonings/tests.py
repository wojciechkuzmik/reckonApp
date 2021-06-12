from django.http import response
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
import json

class GroupsAPITests(APITestCase):

    def setUp(self) :
        self.client = APIClient()
    
    # /api/reckonings/reckoning endpoint tests

    def test_add_new_reckoning_should_respond_201(self):
        data = """
        {
            "name": "Projekt ankiety internetowej",
            "deadline": "2021-05-23T23:03:00Z", 
            "groupid": 30,
            "author": 17
        }
        """
        response = self.client.post('http://127.0.0.1:8000/api/reckonings/reckoning', data, 
            content_type= 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_add_new_reckoning_with_invalid_data_should_respond_400(self):
        data = """
        {
            'name': "Projekt ankiety internetowej",
            'deadline': "2021-05-23T23:03:00Z", 
            "groupid": 30,
            "author": 17
        }
        """
        response = self.client.post('http://127.0.0.1:8000/api/reckonings/reckoning', data, 
            content_type= 'application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_add_new_reckoning_should_add_new_reckoning(self):
        data = """
        {
            "name": "rachunek testowy3",
            "deadline": "2021-05-23T23:03:00Z", 
            "groupid": 30,
            "author": 17
        }
        """
        response = self.client.post('http://127.0.0.1:8000/api/reckonings/reckoning', data, 
            content_type= 'application/json')
        
        self.assertEqual(response.status_code, 201)
        
        json_data = json.loads(response.content.decode())
        self.assertEqual(json_data["name"], "rachunek testowy3")
        self.assertIsNotNone(json_data["deadline"], "2021-05-23T23:03:00Z")
        self.assertIsNotNone(json_data["groupid"], 30)
        self.assertIsNotNone(json_data["author"]), 17

        response = self.client.get('/api/reckonings/reckonings_in_group/30', HTTP_HOST = '127.0.0.1:8000')
        self.assertIn("rachunek testowy3", response.content.decode())

    def test_get_reckoning_info_should_response_200(self):
        response = self.client.get('/api/reckonings/reckoning/51', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)
    
    def test_get_reckoning_info_with_invalid_request_should_response_405(self):
        response = self.client.get('/api/reckonings/reckoning', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 405)
    
    def test_get_reckoning_info_should_respond_with_json(self):
        response = self.client.get('/api/reckonings/reckoning/51', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content.decode())
        self.assertIsNotNone(json_data["reckoningid"])
        self.assertIsNotNone(json_data["name"])
        self.assertIsNotNone(json_data["startdate"])
        self.assertIsNotNone(json_data["deadline"])
        self.assertIsNotNone(json_data["groupid"])
        self.assertIsNotNone(json_data["author"])
        self.assertIsNotNone(json_data["autor"])
        self.assertIsNotNone(json_data["autor_details"])
    
    # /api/reckonings/reckonings_in_group endpoint tests

    def test_get_reckonings_in_group_info_should_response_200(self):
        response = self.client.get('/api/reckonings/reckonings_in_group/30', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)
    
    def test_get_reckonings_in_group_info_with_invalid_request_should_response_404(self):
        response = self.client.get('/api/reckonings/reckonings_in_group', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 404)
    
    def test_get_reckonings_in_group_info_should_response_json(self):
        response = self.client.get('/api/reckonings/reckonings_in_group/30', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content.decode())
        self.assertNotEqual(len(json_data), 0)
        for i in range(len(json_data)):
            self.assertIsNotNone(json_data[i]["reckoningid"])
            self.assertIsNotNone(json_data[i]["name"])
            self.assertIsNotNone(json_data[i]["startdate"])
            self.assertIsNotNone(json_data[i]["deadline"])
            self.assertIsNotNone(json_data[i]["groupid"])
            self.assertIsNotNone(json_data[i]["author"])
            self.assertIsNotNone(json_data[i]["payment_status"])
            self.assertIsNotNone(json_data[i]["author_detail"])
        
    # /api/reckonings/reckoningPosition endpoint tests

    def test_get_reckonings_in_group_by_reckoning_id_should_response_200(self):
        response = self.client.get('/api/reckonings/reckoningPosition/25', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)

    def test_get_reckonings_in_group_by_reckoning_id_with_invalid_request_should_response_405(self):
        response = self.client.get('/api/reckonings/reckoningPosition', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 405)

    def test_get_reckonings_in_group_by_reckoning_id_should_response_json(self):
        response = self.client.get('/api/reckonings/reckoningPosition/51', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content.decode())
        self.assertNotEqual(len(json_data), 0)
        for i in range(len(json_data)):
            self.assertIsNotNone(json_data[i]["reckoningid"])
            self.assertIsNotNone(json_data[i]["name"])
            self.assertIsNotNone(json_data[i]["amount"])
            self.assertIsNotNone(json_data[i]["groupmemberid"])
            self.assertIsNotNone(json_data[i]["reckoningid"])
            self.assertIsNotNone(json_data[i]["author_detail"])

    def test_add_reckoning_position_should_response_201(self):
        data = """
        {
            "name": "kwiate4",
            "amount": 15.0,
            "groupmemberid": 13,
            "reckoningid": 51,
            "paymentdate": "2021-05-23T23:03:00Z"
        }
        """
        response = self.client.post('http://127.0.0.1:8000/api/reckonings/reckoningPosition', data, 
            content_type= 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_add_reckoning_position_with_invalid_data_should_response_400(self):
        data = """
        {
            'name': "kwiate4",
            "amount": 15.0,
            "groupmemberid": 13,
            "reckoningid": 51,
            "paymentdate": "2021-05-23T23:03:00Z"
        }
        """
        response = self.client.post('http://127.0.0.1:8000/api/reckonings/reckoningPosition', data, 
            content_type= 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_add_reckoning_position_should_add_reckoning_position(self):
        data = """
        {
            "name": "kwiate4",
            "amount": 15.0,
            "groupmemberid": 13,
            "reckoningid": 51,
            "paymentdate": "2021-05-23T23:03:00Z"
        }
        """
        response = self.client.post('http://127.0.0.1:8000/api/reckonings/reckoningPosition', data, 
            content_type= 'application/json')
        self.assertEqual(response.status_code, 201)
        json_data = json.loads(response.content.decode())
        self.assertEqual(json_data["name"], "kwiate4")
        self.assertEqual(json_data["amount"], 15.0)
        self.assertEqual(json_data["reckoningid"], 51)
        self.assertEqual(json_data["paymentdate"], "2021-05-23T23:03:00Z")
        
        response = self.client.get(
            'http://127.0.0.1:8000/api/reckonings/GroupMemberUser/'+str(json_data["groupmemberid"]),
            content_type= 'application/json')
        json_data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data["userid"], 13)



    # /api/reckonings/reckoningPositionsForUser endpoint tests

    def test_get_reckon_info_for_user_should_response_200(self):
        response = self.client.get('/api/reckonings/reckoningPositionsForUser/17', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)
    
    def test_get_reckon_info_for_user_with_invalid_request_should_response_404(self):
        response = self.client.get('/api/reckonings/reckoningPositionsForUser', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 404)
    
    def test_get_reckon_info_for_user_should_response_with_json(self):
        response = self.client.get('/api/reckonings/reckoningPositionsForUser/13', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content.decode())
        self.assertNotEqual(len(json_data), 0)
        for i in range(len(json_data)):
            self.assertIsNotNone(json_data[i]["reckoningid"])
            self.assertIsNotNone(json_data[i]["name"])
            self.assertIsNotNone(json_data[i]["amount"])
            self.assertIsNotNone(json_data[i]["groupmemberid"])
            self.assertIsNotNone(json_data[i]["reckoningid"])
            # self.assertIsNotNone(json_data[i]["paymentdate"])
            self.assertIsNotNone(json_data[i]["author_detail"])

    # /api/reckonings/reckoningPositionsByUser endpoint tests

    def test_get_reckon_owner_info_for_user_should_response_200(self):
        response = self.client.get('/api/reckonings/reckoningPositionsByUser/41', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)
    
    def test_get_reckon_owner_info_for_user_with_invalid_request_should_response_404(self):
        response = self.client.get('/api/reckonings/reckoningPositionsByUser', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 404)

    def test_get_reckon_owner_info_for_user_should_response_with_json(self):
        response = self.client.get('/api/reckonings/reckoningPositionsByUser/17', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content.decode())
        self.assertNotEqual(len(json_data), 0)
        for i in range(len(json_data)):
            self.assertIsNotNone(json_data[i]["reckoningid"])
            self.assertIsNotNone(json_data[i]["name"])
            self.assertIsNotNone(json_data[i]["amount"])
            self.assertIsNotNone(json_data[i]["groupmemberid"])
            self.assertIsNotNone(json_data[i]["reckoningid"])
            # self.assertIsNotNone(json_data[i]["paymentdate"])
            self.assertIsNotNone(json_data[i]["author_detail"])

    # /api/reckonings/UpdateReckoningStatusView endpoint tests

    def test_update_reckoning_status_should_response_200(self):
        data = """
        {
            "reckoningpositionid": 134
        }
        """
        response = self.client.put('http://127.0.0.1:8000/api/reckonings/UpdateReckoningStatusView', data, 
            content_type= 'application/json')
        
    def test_update_reckoning_status_should_update_paymentinfo(self):
        response = self.client.get('/api/reckonings/reckoningPosition/25', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content.decode())
        for el in json_data:
            if el["reckoningpositionid"] == 134:
                self.assertIsNone(el["paymentdate"])
        
        data = """
        {
            "reckoningpositionid": 134
        }
        """
        response = self.client.put('http://127.0.0.1:8000/api/reckonings/UpdateReckoningStatusView', data, 
            content_type= 'application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/reckonings/reckoningPosition/25', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content.decode())
        for el in json_data:
            if el["reckoningpositionid"] == 89:
                self.assertIsNotNone(el["paymentdate"])


    