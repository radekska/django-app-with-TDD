from django.test import TestCase
from unittest.mock import patch
from accounts.models import Token

import accounts.views

class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.post(
            path='/accounts/send_login_email', data={
                'email': 'testredirects@example.com'
            }
        )
        self.assertRedirects(response, '/')


    def test_sends_mail_to_address_from_post(self):
        self.send_email_called = False

        def fake_send_email(subject, body, from_email, to_list_email):
            self.send_email_called = True
            self.subject = subject
            self.body = body
            self.from_email = from_email
            self.to_list_email = to_list_email

        accounts.views.send_mail = fake_send_email
        self.client.post(path='/accounts/send_login_email', data={
            'email': 'testredirects@example.com'
        })

        self.assertTrue(self.send_email_called)
        self.assertEqual(self.subject, 'Your login link for Superlists')
        self.assertEqual(self.from_email, 'noreply@superlists.com')
        self.assertEqual(self.to_list_email, ['testredirects@example.com'])


    # patch decorator will take send_mail Django function and automagically generate a mock funtion based on given one.
    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post_v2(self, mock_send_mail):
        self.client.post(path='/accounts/send_login_email', data={
            'email': 'testredirects@example.com'
        })

        self.assertTrue(mock_send_mail.called)
        (subjcet, body, from_email, to_list_email), kwargs = mock_send_mail.call_args
        self.assertEqual(subjcet, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists.com')
        self.assertEqual(to_list_email, ['testredirects@example.com'])


    def test_adds_success_message(self):
        response = self.client.post(
            path='/accounts/send_login_email', data={
            'email': 'testredirects@example.com'
            }, follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in."
        )
        self.assertEqual(message.tags, 'success')

class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.get(
            path='/accounts/login?token=abc123'
        )
        self.assertRedirects(response, '/')

    def test_creates_token_associated_with_email(self):
        self.client.post(path='/accounts/send_login_email', data={
            'email': 'test@example.com'
        })
        token = Token.objects.first()
        self.assertEqual(token.email, 'test@example.com')
    
    @patch('accounts.views.send_mail')
    def test_sends_login_link_using_token_uuid(self, mock_send_email):
        self.client.post(path='/accounts/send_login_email', data={
            'email': 'test@example.com'
        })
        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subjcet, body, from_email, to_list_email), kwargs = mock_send_email.call_args
        self.assertIn(expected_url, body)

