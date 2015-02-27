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


if __name__ == '__main__':
  unittest.main()

"""
1) Может быть я не понял интерфейса github, но я не увидел, включён ли файл с tld-доменами в один из коммитов. Файл не должен скачиваться, он должен быть в составе библиотеки tools.

2) Тестов нужно больше, нужно протестировать следующие случаи:
2-0) 192.168.0.1
2-0) http://192.168.0.1
2-0) http://999.999.999.999
2-0) 123.123.123
2-0) 12345
2-0) None
2-0) "" (пустая строка)
2-1) domain.com
2-2) domain.foobar
2-3) domain.com/path
2-4) domain.com/path?foo=bar
2-5) /path
2-6) /path?foo=bar
2-7) foobar
2-8) http://domain.com
2-9) http://domain.foobar
2-10) asdf://domain.com
2-11) asdf://domain.foobar
2-12) http://domain.com/foobar
2-13) http://domain.foobar/foobar
2-14) http://domain.com/foobar?foo=bar
2-15) http://домен.рф
2-16) http://домен.фубар
2-17) http://домен.рф/foobar
2-18) http://домен.рф/фубар
2-19) http://домен.рф/фубар?foo=bar
2-20) http://домен.рф/фубар?фуу=бар

Нужно тестироваь буквально эти урлы, это не абстрактные примеры, а конкретные случаи для тестирования. Я без понятия, как будут обработаны некоторые из этих примеров, предлагаю написать тесты и посмотреть :) На каждый тест отдельная функция т.е. не надо 20 проверок в одну фукнцию пихать, надо 20 test_* функций создать.
"""