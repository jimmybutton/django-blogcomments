from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post, Comment

class BlogTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='samuel',
            email='user@email.com',
            password='secret',
        )

        self.post = Post.objects.create(
            title="First post",
            author=self.user,
            body="Some text about travelling the world"
        )

        self.comment = Comment.objects.create(
            post = self.post,
            name = "John Doe",
            comment = "A comment on this post"
        )
    
    def test_post_list(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First post')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First post')
        self.assertContains(response, 'Some text about travelling the world')
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'A comment on this post')
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_submit_comment_logged_in(self):
        self.client.login(username='samuel', password='secret')
        url = reverse('post_detail', args=[1])
        response = self.client.post(url, {
            'name': 'Samuel',
            'comment': 'Thanks for your feedback'
        })
        self.assertEqual(response.status_code, 302)  # Found redirect
        self.assertEqual(Comment.objects.last().name, 'Samuel')
        self.assertEqual(Comment.objects.last().comment, 'Thanks for your feedback')
    

    def test_submit_comment_logged_out_fail(self):
        self.client.logout()
        url = reverse('post_detail', args=[1])
        response = self.client.post(url, {
            'name': 'Samuel', 
            'comment': 'I am not the real author',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, you cannot use this name.")
    
    def test_submit_comment_logged_out_success(self):
        self.client.logout()
        url = reverse('post_detail', args=[1])
        response = self.client.post(url, {
            'name': 'Peter',
            'comment': "I definitely have to try this!"
        })
        self.assertEqual(response.status_code, 302)  # Found redirect
        self.assertEqual(Comment.objects.last().name, 'Peter')
        self.assertEqual(Comment.objects.last().comment, "I definitely have to try this!")