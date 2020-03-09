from rest_framework.authtoken.models import Token
from test_plus import APITestCase
import faker


class TestRest(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = self.make_user("user1")
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.faker = faker.Faker()


    def _create_account(self):
        data = dict(name="andres", external_id=1)
        self.post("account-list",data=data)
        self.response_201()
        return self.last_response.json()

    def test_create(self):
        self.get_check_200("account-list")

        resp = self._create_account()

        id =  resp.get("id", False)
        self.assertTrue(id, resp)

        self.get("account-hosts-list", accounts_pk=id)
        self.response_200()
        data = {
            'type':self.faker.random_element(elements=("ping","black")),
            'hostname':self.faker.domain_name(),
        }
        self.post("account-hosts-list", accounts_pk=id, data=data)
        host_id = self.last_response.json().get("id")
        self.get("account-hosts-detail", accounts_pk=id, pk = host_id)
        self.response_200()
        resp = self.last_response.json()




