from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from wall.models import Post


user_list_path = reverse('user-list')
class PostModelTest(TestCase):
    def setUp(self):
        self.client.post(user_list_path,
                         {'username': 'test_user',
                          'email': 'test_user@example.com',
                          'password': 'test_user'})

        user = User.objects.first()
        Post.objects.create(body='test content', author=user)

    # Unit Tests
    def test_body_label(self):
        post = Post.objects.first()
        field_label = post._meta.get_field('body').verbose_name
        self.assertEquals(field_label, 'Body')

    def test_author_label(self):
        post = Post.objects.first()
        field_label = post._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    def test_post_author_is_instance_of_user(self):
        post = Post.objects.first()
        self.assertTrue(isinstance(post.author, User))

    # Behaviour tests
    def test_cannot_create_post_if_body_empty(self):
        user = User.objects.first()
        post = Post(author=user, body='')
        self.assertRaises(ValidationError, lambda: post.save())
