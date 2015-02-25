# coding: utf-8
from unittest import TestCase

from tools.http import normalize_url
from tools.error import InvalidUrlError

class HttpTestCase(TestCase):
    def test_idn(self):
        url = u'http://почта.рф/path?arg=val'
        idn_url = 'http://xn--80a1acny.xn--p1ai/path?arg=val'
        self.assertEqual(idn_url, normalize_url(url))

    def test_idn_in_params(self):
        url = u'http://ru.wikipedia.org/w/index.php?title=Заглавная_страница'
        idn_url = 'http://ru.wikipedia.org/w/index.php?title=' \
                '%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_' \
                '%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'
        self.assertEqual(idn_url, normalize_url(url))

    def test_invalid_url(self):
        invalid_url = 'http://13354&altProductId=6423589&productId=6423589'\
                      '&altProductStoreId=13713&catalogId=10001'\
                      '&categoryId=28678&productStoreId=13713'\
                      'http://www.textbooksnow.com/webapp/wcs/stores'\
                      '/servlet/ProductDisplay?langId=-1&storeId='
        self.assertRaises(InvalidUrlError, normalize_url, invalid_url)