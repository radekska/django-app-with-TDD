from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = 'testemail@example.com'
SUBJCET = 'Your login link for Superlists'


class PasswordlessAuthenticationTest(FunctionalTest):
    
    def test_can_generate_uid_and_send_email(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        self.wait_for(lambda : self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
            ))

        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(SUBJCET, email.subject)

        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')

        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        self.browser.get(url)
        self.wait_for(
            lambda : self.browser.find_element_by_link_text('Log out')
        )

        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)