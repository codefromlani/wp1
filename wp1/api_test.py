import sys
import unittest
from unittest.mock import MagicMock, patch

import mwclient

from wp1 import api

class ApiTest(unittest.TestCase):
  def setUp(self):
    self.page = MagicMock()

  def test_login_called_when_import_creds(self):
    api.site = MagicMock()
    mock_credentials = MagicMock()
    sys.modules['wp1.credentials'] = mock_credentials
    api.login()
    self.assertEqual(1, api.site.login.call_count)

  def test_login_exception_when_import_creds(self):
    api.logger = MagicMock()
    api.site = MagicMock()
    mock_credentials = MagicMock()
    api.site.login.side_effect = mwclient.errors.LoginError()
    api.login()
    self.assertEqual(1, api.logger.exception.call_count)

  def test_save_page(self):
    api.site = MagicMock()
    api.save_page(self.page, '<code>', 'edit summary')
    self.assertEqual(1, len(self.page.save.call_args_list))
    self.assertEqual(('<code>', 'edit summary'), self.page.save.call_args[0])

  @patch('wp1.api.login')
  def test_save_page_tries_login_on_exception(self, patched_login):
    api.site = MagicMock()
    self.page.save.side_effect = mwclient.errors.AssertUserFailedError()
    with self.assertRaises(mwclient.errors.AssertUserFailedError):
      actual = api.save_page(self.page, '<code>', 'edit summary')
      self.assertTrue(actual)
      self.assertEqual(1, len(patched_login.call_args_list))

  def test_save_page_skips_login_on_none_site(self):
    api.site = None
    actual = api.save_page(self.page, '<code>', 'edit summary')
    self.assertFalse(actual)
