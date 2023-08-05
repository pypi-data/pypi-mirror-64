""" Unit tests for crackle_api_helpers """
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
from __future__ import print_function

import os
import unittest
from collections import namedtuple
from phoenix_api_helpers.api_wrapper import AuthHelpers
from extensions.yaml_parser import YamlParser


class TestHelpers(unittest.TestCase):
    """ Test all helper methods """

    def setUp(self):
        """ Set up tasks for tests """
        self.environment = os.getenv('environment', 'staging').lower()
        yaml = YamlParser(
            'phoenix_api_helpers/environment_config.yaml').data(
            self.environment)
        apiconfig = namedtuple('apiconfig',
                               'host tenant_id platform_id data_id secret')
        self.config = apiconfig(
            host=os.getenv('host', yaml['host']),
            tenant_id=os.getenv('tenant_id', yaml['tenant_id']),
            platform_id=os.getenv('platform_id', yaml['platform_id']),
            data_id=os.getenv('data_id', yaml['data_id']),
            secret=os.getenv('secret', yaml['secret']))

        self.auth_helpers = AuthHelpers(self.config)

    def test_generate_auth_token(self):
        """ Test generate auth token """
        print('testing generate_auth_token')
        self.assertIsNotNone(self.auth_helpers.generate_auth_token(), "failed with auth token not generated")

    def test_register_user(self):
        """ Test register a new user """
        print('testing register_user')
        status_code, email_address, password, user_id, user_token = \
            self.auth_helpers.register_user()
        assert status_code == 201, "failed with status code: {0}".format(status_code)
        assert email_address != '', "failed with empty email_address field"
        assert password != '', "failed with empty password field"
        assert user_id != '', "failed with empty user_id field"
        assert user_token != '', "failed with empty user_token field"

    def test_add_user_watching_feed(self):
        """ Test add watch feed for a user """
        print('testing add_user_watch_feed')
        status_code = self.auth_helpers.add_user_watch_feed(feed_type='continue')
        assert status_code == 201, "failed with status code: {0}".format(status_code)


if __name__ == '__main__':
    unittest.main()
