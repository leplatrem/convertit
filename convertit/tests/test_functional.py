import os
import shutil
import urllib2

from mock import Mock, patch
from webtest import TestApp

from convertit import main
from convertit.tests.unittest import unittest


here = os.path.dirname(__file__)
data_path = os.path.join(here, 'data')
settings = {
    'convertit.downloads_path': os.path.join(data_path, 'downloads'),
    'convertit.downloads_max_age': 60,
    'convertit.converted_path': os.path.join(data_path, 'converted'),
    'convertit.converted_max_age': 60,
    'convertit.converted_url': 'converted',
    'convertit.converted_name': '{url_hostname}_{url_port}_{url_dirname}_{url_filename}{extension}',
    'convertit.converters': """
        convertit.converters.unoconv
        convertit.converters.inkscape
    """,
}


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        app = main({}, **settings)
        self.testapp = TestApp(app)

    def tearDown(self):
        shutil.rmtree(settings['convertit.converted_path'])
        shutil.rmtree(settings['convertit.downloads_path'])

    def odt_data(self):
        odt_path = os.path.join(data_path, 'test_document.odt')
        return open(odt_path).read()

    def test_no_url(self):
        "Get homepage without any `url` param"

        resp = self.testapp.get('/', status=400)
        self.assertTrue('Missing parameter' in resp.body)

    def test_with_valid_url(self):
        "Get homepage with valid `url` param"

        url = 'http://example.com/test_document.odt'
        with patch.object(urllib2, 'urlopen') as mock_urlopen:
            mock_req = Mock()
            mock_req.read.return_value = self.odt_data()
            mock_urlopen.return_value = mock_req
            resp = self.testapp.get('/', params={'url': url}, status=302)
            mock_urlopen.assert_called_once_with(url)
            filename = os.path.basename(resp.location)
            filepath = os.path.join(settings['convertit.converted_path'],
                                    filename)
            self.assertTrue(os.path.exists(filepath))

    def test_with_valid_url_toword(self):
        "Get homepage with valid `url` param"

        url = 'http://example.com/test_document.odt'
        converted_path = settings['convertit.converted_path']
        with patch.object(urllib2, 'urlopen') as mock_urlopen:
            mock_req = Mock()
            mock_req.read.return_value = self.odt_data()
            mock_urlopen.return_value = mock_req
            request_params = {'url': url, 'to': 'application/msword'}
            resp = self.testapp.get('/', params=request_params, status=302)
            mock_urlopen.assert_called_once_with(url)
            filename = os.path.basename(resp.location)
            filepath = os.path.join(converted_path, filename)
            self.assertTrue(os.path.exists(filepath))

    def test_invalid_url_type(self):
        "Get homepage with `url` missing a protocol identifier"
        url = 'www.example.com/test_document.odt'
        resp = self.testapp.get('/', params={'url': url}, status=400)
        self.assertTrue("unknown url type" in resp.body)

    def test_no_such_transform(self):
        "Get homepage with `url` that triggers a DNS resolution error"
        url = 'http://example.com/test_document.odt'
        with patch.object(urllib2, 'urlopen') as mock_urlopen:
            mock_req = Mock()
            mock_req.read.return_value = self.odt_data()
            mock_urlopen.return_value = mock_req

            request_params = {'url': url, 'to': 'application/pdfnocontent'}
            resp = self.testapp.get('/', params=request_params, status=400)

            self.assertTrue('Unsupported transform' in resp.body)

    def test_invalid_hostname(self):
        "Get homepage with `url` that triggers a DNS resolution error"
        with patch.object(urllib2, 'urlopen') as mock_urlopen:
            url = 'http://example.com/test_document.odt'
            message = "Name or service not known"
            mock_urlopen.side_effect = urllib2.URLError(message)
            resp = self.testapp.get('/', params={'url': url}, status=400)
            self.assertTrue("Name or service not known" in resp.body)

    def test_forbidden_url(self):
        "Get homepage with `url` that is forbidden"
        with patch.object(urllib2, 'urlopen') as mock_urlopen:
            url = 'http://example.com/test_document.odt'
            mock_urlopen.side_effect = urllib2.HTTPError(url, 403,
                                                         "Forbidden access",
                                                         [], None)
            resp = self.testapp.get('/', params={'url': url}, status=403)
            self.assertTrue("Forbidden access" in resp.body)

    def test_post(self):
        "Get post document"
        upload_files = [('file', 'test_document.odt', self.odt_data())]
        converted_path = settings['convertit.converted_path']
        resp = self.testapp.post('/', upload_files=upload_files, status=302)
        filename = os.path.basename(resp.location)
        filepath = os.path.join(converted_path, filename)
        self.assertTrue(os.path.exists(filepath))
