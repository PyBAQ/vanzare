from rest_framework.test import APITestCase

# Create your tests here.


class TestBase(APITestCase):

    API_URL = '/api/v1/'
    ENDPOINT = ''

    def get(self, params=''):
        return self.client.get(f'{self.API_URL}{self.ENDPOINT}', params, format='json')

    def retrive(self, _id):
        return self.client.get(f'{self.API_URL}{self.ENDPOINT}{_id}/')

    def create(self, payload):
        return self.client.post(f'{self.API_URL}{self.ENDPOINT}', payload, format='json')

    def update(self, payload):
        _id = payload.get('id')
        return self.client.put(f'{self.API_URL}{self.ENDPOINT}{_id}/',
                               payload, sformat='json')

    def delete(self):
        raise NotImplementedError("To be implemented")
