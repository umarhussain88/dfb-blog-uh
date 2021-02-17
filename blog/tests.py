from django import test
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your tests here.

from .models import Post 

class BlogTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username ='testuser', 
            email='test@email.com',
            password='secret'
        )

        #constants. 
        self.m_title = "A pretty damn good title!"
        self.m_body = "Nice Body Content"

        self.post = Post.objects.create(

            title=self.m_title,
            body=self.m_body,
            author=self.user 
        )


    def test_string_representation(self):
        post = Post(title="A Sample Title")
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f"{self.post.title}", self.m_title)    
        self.assertEqual(f"{self.post.author}", "testuser")    
        self.assertEqual(f"{self.post.body}", self.m_body)    


    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, self.m_body)
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1')
        no_response = self.client.get('/post/999')
        self.assertEqual(response.status_code,200)
        self.assertEqual(no_response.status_code,404)
        self.assertContains(response, self.m_title)
        self.assertTemplateUsed(response,'post_detail.html')

