from django.contrib.auth import get_user_model
from django.urls import reverse


class UnittestAuthenticationMixin:
    """Mixin to authenticate a user in unit tests"""

    def authenticate(self) -> str | None:
        user_model = get_user_model()

        user = user_model.objects.first()
        if user is not None:
            user.set_password('touparet')
            user.save()

            path = reverse('token_obtain_pair')
            response = self.client.post(path, {
                'username': user.username,
                'password': 'touparet'
            })

            self.assertEqual(response.status_code, 200)

            token = response.json()['access']
            self.client.headers = {'HTTP_AUTHORIZATION': f'Token {token}'}
            return token
        return None
