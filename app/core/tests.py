from rest_framework.authtoken.models import Token
from test_plus import APITestCase


class TestRest(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = self.make_user("user1")
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


    def _create_account(self):
        data = dict(  name="andres", external_id=1)
        self.post("account-list",data=data)
        self.response_201()
        return self.last_response.json()

    def test_create(self):
        resp = self._create_account()
        assert resp.get("id")
        
