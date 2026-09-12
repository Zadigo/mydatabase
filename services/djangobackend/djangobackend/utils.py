from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient


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


def authenticated_client():
    user_model = get_user_model()
    user_model.objects.create_user(username='testuser', password='touparet')

    user = user_model.objects.first()
    if user is None:
        raise ValueError("User creation failed")
    
    if user is not None:
        user.set_password('touparet')
        user.save()

    client = APIClient()
    path = reverse('token_obtain_pair')
    response = client.post(
        path, {
            'username': user.username,
            'password': 'touparet'
        }
    )

    assert response.status_code == 200

    token = response.json()['access']
    client.headers = {'HTTP_AUTHORIZATION': f'Token {token}'}
    return client
