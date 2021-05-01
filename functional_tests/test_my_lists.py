from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenitcated_session


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenitcated_session(email)
        
        self.browser.get(self.live_server_url + '/404_not_found/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/'
        ))
        
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'test@example.com'
        self.create_pre_authenticated_session(email)

        self.browser.get(self.live_server_url)
        self.add_list_item('Item one test')
        self.add_list_item('Item two test')
        first_list_url = self.browser.current_url

        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Item one test')            
        )
        self.browser.find_element_by_link_text('Item one test').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        self.browser.get(self.live_server_url)
        self.add_list_item('Item three for new list')
        second_list_url = self.browser.current_url

        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Item three for new list')            
        )
        self.browser.find_element_by_link_text('Item three for new list').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )
    
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for( lambda: self.assertEqual(
            self.browser.find_element_by_link_text('My lists'),
            list()
        ))
    