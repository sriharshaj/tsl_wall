from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from rest_framework import status

from wall.models import Post
from wall.serializers import UserSerializerWithToken

no_of_posts = 10
post_list_path = reverse('post-list')
user_list_path = reverse('user-list')
current_user_path = reverse('current-user')

class PostListViewTest(TestCase):
    def setUp(self):
        self.user = {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': 'test_user'

        }
        serializer = UserSerializerWithToken(data=self.user)
        if serializer.is_valid():
            serializer.save()
        self.jwt_token = 'JWT ' + serializer.data['token']

        user = User.objects.first()
        for _ in range(no_of_posts):
            Post.objects.create(body='random body', author=user)

    # Unit Tests
    def test_posts_list_view(self):
        response = self.client.get(post_list_path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_list_response_return_body_and_author(self):
        response = self.client.get(post_list_path)
        post_dict_keys = response.data[0].keys()
        self.assertIn('body', post_dict_keys)
        self.assertIn('author', post_dict_keys)

    def test_current_user_view(self):
        auth_headers = {'HTTP_AUTHORIZATION': self.jwt_token}
        response = self.client.get(current_user_path, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_current_user_return_username_and_email(self):
        auth_headers = {'HTTP_AUTHORIZATION': self.jwt_token}
        response = self.client.get(current_user_path, **auth_headers)
        user_dict_keys = response.data.keys()
        self.assertIn('username', user_dict_keys)
        self.assertIn('email', user_dict_keys)

    def test_user_list_view(self):
        user = {
            'username': 'test_user1',
            'email': 'test_user1@example.com',
            'password': 'test_user1'

        }
        response = self.client.post(user_list_path, user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_list_return_username_and_email_and_token(self):
        user = {
            'username': 'test_user1',
            'email': 'test_user1@example.com',
            'password': 'test_user1'
        }
        response = self.client.post(user_list_path, user)
        user_dict_keys = response.data.keys()
        self.assertIn('username', user_dict_keys)
        self.assertIn('email', user_dict_keys)
        self.assertIn('token', user_dict_keys)

    # Behaviour tests
    def test_anonymous_user_can_retrive_all_posts(self):
        response = self.client.get(post_list_path)
        self.assertEqual(len(response.data), no_of_posts)

    def test_signed_user_can_retrive_all_posts(self):
        auth_headers = {'HTTP_AUTHORIZATION': self.jwt_token}
        response = self.client.get(post_list_path,  **auth_headers)
        self.assertEqual(len(response.data), no_of_posts)

    def test_anonymous_user_cannot_create_post(self):
        response = self.client.post(post_list_path, {'body': 'Hacked you'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_signed_user_can_create_post(self):
        post_body = 'Hacked You'
        auth_headers = {'HTTP_AUTHORIZATION': self.jwt_token}
        response = self.client.post(
            post_list_path, {'body': post_body}, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['body'], post_body)
        self.assertEqual(response.data['author']['username'],
                         self.user['username'])
