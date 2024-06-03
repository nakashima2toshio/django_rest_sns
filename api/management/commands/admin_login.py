
import pprint

from rest_framework.test import APIClient
from django.core.management import BaseCommand
from api.models import CustomUser


class Command(BaseCommand):
    help = '[Usage] admin_login check'

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.user = None
        self.username = None
        self.password = None
        self.client = APIClient()

    def handle(self, *args, **options):
        # setup
        self.username = "admin"
        self.password = "Tn1021$tn1021"

        # Check if the user already exists, if not create one
        try:
            self.user = CustomUser.objects.get(username=self.username)
        except CustomUser.DoesNotExist:
            self.user = CustomUser.objects.create_user(username=self.username, password=self.password)

        # CSRFトークンは不要なので削除して、
        # ログインリクエストを送信
        login_response = self.client.post('/api/login/', {"username": self.username, "password": self.password},
                                          format='json')

        print(login_response.status_code)  # 200 OK
        pprint.pprint(login_response)
        print('token', login_response.data)  # レスポンスに token が含まれていることを確認


