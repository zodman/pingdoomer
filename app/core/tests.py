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
        data = dict(name=self.faker.name(),
                    external_id=self.faker.random_digit())
        self.post("account-list",data=data)
        self.response_201()
        return self.last_response.json()

    def _create_hosts(self):
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
        self.response_201()
        return id, self.last_response.json()

    def test_create(self):
        self._create_account()

    def test_create_host(self):
        resp = self._create_hosts()

    def test_host_detail(self):
        id, resp = self._create_hosts()
        host_id = resp.get("id")
        self.get("account-hosts-detail", accounts_pk=id, pk = host_id)

        self.response_200()
        resp = self.last_response.json()
        self.assertTrue(resp)
    def _create_contact(self):
        id, _ = self._create_hosts()
        self.get_check_200("account-contacts-list", accounts_pk=id)

        data = {
            'name': self.faker.name(),
            'phone': self.faker.phone_number(),
            'email': self.faker.email()
        }

        self.post("account-contacts-list", accounts_pk=id, data=data)
        self.response_201()
        resp = self.last_response.json()
        return resp


    def test_create_alerts(self):
        resp = self._create_contact()
        contact_id = resp.get("id")
        self.get_check_200("contact-alerts-list", accounts_pk=id, contacts_pk=contact_id)



















