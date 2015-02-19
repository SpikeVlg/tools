# coding: utf-8
from unittest import TestCase

from tools.http import normalize_url

class HttpTestCase(TestCase):
    def test_idn(self):
        url = 'http://почта.рф/path?arg=val'
        idn_url = 'http://xn--80a1acny.xn--p1ai/path?arg=val'
        self.assertEqual(idn_url, normalize_url(url))

    def test_idn_in_params(self):
        url = 'http://ru.wikipedia.org/w/index.php?title=Заглавная_страница'
        idn_url = 'http://ru.wikipedia.org/w/index.php?xn--title=_-7fgaabawm2dxa9bzbd2duw0h2j'
        self.assertEqual(idn_url, normalize_url(url))
