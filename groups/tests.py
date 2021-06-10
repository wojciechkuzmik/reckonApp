from rest_framework.test import APITestCase
from rest_framework.test import APIClient
import json

class GroupsAPITests(APITestCase):
    def setUp(self) :
        self.client = APIClient()

    # /api/groups/group endpoint tests
    # create new group tests

    def test_create_new_group_should_response_201(self):  
        data = """
        {
            "name": "klaster_testowy"
        }
        """  
        response = self.client.post('http://127.0.0.1:8000/api/groups/group', data, 
            content_type= 'application/json')
        self.assertEqual(response.status_code, 201)
    
    def test_create_new_group_with_invalid_data_should_response_400(self):  
        data = """
        {
            'name': "klaster_testowy"
        }
        """  
        response = self.client.post('http://127.0.0.1:8000/api/groups/group', data, 
            content_type= 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_new_group_should_create_new_group(self):  
        data = """
        {
            "name": "klaster_testowy"
        }
        """  
        response = self.client.post('http://127.0.0.1:8000/api/groups/group', data, 
            content_type= 'application/json')
        self.assertEqual(response.status_code, 201)

        json_data = json.loads(response.content.decode())
        groupid = json_data["groupid"]
        response = self.client.get('/api/groups/group/'+str(groupid), HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content.decode())
        self.assertEqual(json_data["name"], "klaster_testowy")
    
    # update group name tests

    def test_update_group_name_should_respond_204(self):
        data = """
        {
            "name": "nowa_nazwa_klaster_testowy"
        }
        """  
        response = self.client.patch('http://127.0.0.1:8000/api/groups/group/16', data, 
            content_type= 'application/json')
        self.assertEqual(response.status_code, 204)
    
    def test_update_group_name_with_invalid_data_should_respond_400(self):
        data = """
        {
            'name': 'nowa_nazwa_klaster_testowy'
        }
        """  
        response = self.client.patch('http://127.0.0.1:8000/api/groups/group/16', data, 
            content_type= 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_group_name_should_update_name(self):
        data = """
        {
            "name": "klaster_testowy"
        }
        """  
        response = self.client.post('http://127.0.0.1:8000/api/groups/group', data, 
            content_type= 'application/json')
        self.assertEqual(response.status_code, 201)

        json_data = json.loads(response.content.decode())
        groupid = json_data["groupid"]
        response = self.client.get('/api/groups/group/'+str(groupid), HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content.decode())
        self.assertEqual(json_data["name"], "klaster_testowy")
        data = """
        {
            "name": "nowa_nazwa_klaster_testowy"
        }
        """  
        response = self.client.patch('http://127.0.0.1:8000/api/groups/group/'+str(groupid), data, 
            content_type= 'application/json')
        self.assertEqual(response.status_code, 204)

        response = self.client.get('/api/groups/group/'+str(groupid), HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content.decode())
        self.assertEqual(json_data["name"], "nowa_nazwa_klaster_testowy")

    # get group info tests

    def test_get_group_info_by_groupid_should_response_200(self):
        response = self.client.get('/api/groups/group/16', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)
    
    def test_get_group_info_by_groupid_with_invalid_request_should_response_404(self):
        response = self.client.get('/api/groups/group/', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 404)
    
    def test_get_group_info_by_groupid_response_should_be_json(self):
        response = self.client.get('/api/groups/group/16', HTTP_HOST = '127.0.0.1:8000')
        response_dict = json.loads(response.content)
        self.assertEqual(response_dict["groupid"], 16)
        self.assertIsNotNone(response_dict["name"])
        self.assertIsNotNone(response_dict["startdate"])
        self.assertIsNotNone(response_dict["members"])

    # /api/groups/groupinfo endpoint tests

    def test_get_all_groups_by_userid_should_response_200(self):
        response = self.client.get('/api/groups/groupinfo/2', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)
    
    def test_get_all_groups_by_userid_with_invalid_request_should_response_404(self):
        response = self.client.get('/api/groups/groupinfo', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 404)
    
    def test_get_all_groups_by_userid_should_response_with_json(self):
        response = self.client.get('/api/groups/groupinfo/17', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.content.decode())

        self.assertNotEqual(len(json_data), 0)

        self.assertIsNotNone(json_data[0]["groupid"])
        self.assertIsNotNone(json_data[0]["name"])
        self.assertIsNotNone(json_data[0]["startdate"])

        self.assertNotEqual(len(json_data[0]["members"]), 0)

        for user in json_data[0]["members"]:
            self.assertIsNotNone(user["userid"])
            self.assertIsNotNone(user["firstname"])
            self.assertIsNotNone(user["lastname"])
            self.assertIsNotNone(user["email"])

    # /api/groups/groupmembers endpoint tests
    
    def test_get_all_groupmembers_by_groupid_should_response_200(self):
        response = self.client.get('/api/groups/groupmembers/2', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)

    def test_get_all_groupmembers_by_groupid_should_response_with_json(self):
        response = self.client.get('/api/groups/groupmembers/5', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.content.decode())

        self.assertNotEqual(len(json_data), 0)

        for user in json_data:
            self.assertIsNotNone(user["groupmemberid"])
            self.assertIsNotNone(user["groupid"])
            self.assertIsNotNone(user["userid"])
            self.assertIsNotNone(user["adddate"])
    
    def test_get_all_groupmembers_by_groupid_with_invalid_request_should_response_404(self):
        response = self.client.get('/api/groups/groupmembers/', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 404)

    def test_add_user_to_group_should_response_201(self):
        data = """
        {
            "groupid": 30,
            "userid": 7
        }
        """  
        response = self.client.post('http://127.0.0.1:8000/api/groups/groupmembers', data, 
            content_type= 'application/json')
        self.assertEqual(response.status_code, 201)
    
    def test_add_user_to_group_should_add_user(self):
        data = """
        {
            "groupid": 30, 
            "userid": 7
        }
        """  
        response = self.client.post('http://127.0.0.1:8000/api/groups/groupmembers', data, 
            content_type= 'application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/api/groups/groupmembers/30', HTTP_HOST = '127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)

        tmp = 0
        json_data = json.loads(response.content.decode())
        for el in json_data:
            if el["userid"] == 13:
                self.assertEqual(el["userid"], 13)
                tmp += 1
        
        self.assertGreaterEqual(tmp, 1)

    def test_delete_user_from_group_should_response_204(self):
        response = self.client.delete('http://127.0.0.1:8000/api/groups/groupmembers/53')
        self.assertEqual(response.status_code, 204)

    def test_delete_user_from_group_should_response_404(self):
        response = self.client.delete('http://127.0.0.1:8000/api/groups/groupmembers/5')
        self.assertEqual(response.status_code, 404)
    
    def test_delete_user_from_group_should_delete_user(self):
        response = self.client.delete('http://127.0.0.1:8000/api/groups/groupmembers/53')
        self.assertEqual(response.status_code, 204)

        response = self.client.get('http://127.0.0.1:8000/api/groups/groupmembers/53')
        self.assertEqual(response.status_code, 200)
