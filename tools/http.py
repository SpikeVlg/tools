import os
try:
    import urllib.parse as urllib
except ImportError:
    import urllib
try:
    from urlparse import urlsplit
except ImportError:
    from urllib.parse import urlsplit
import re
import logging

from tools.error import RuntimeConfigError
from tools.encoding import smart_str, smart_unicode

from tools.py3k_support import *

# I do not know, what the hell is going on, but sometimes
# when IDN url should be requested grab fails with error
# LookupError: unknown encoding: punycode
# That happens in grab/base.py near by 347 line on the line::
# kwargs['url'] = normalize_url(kwargs['url'])
# If you try to catch the error with except and import pdb; pdb.set_trace()
# then you'll get "no pdb module" error. WTF??
# But if you import pdb at the top of the module then you can use it
# So.... I import here this module and I hope that will helps
# My idea is that some mystical shit does some thing that breaks python
# environment,, breaks sys.path So, when special case occurs and some new module
# is need to be imported then that can't be done due to the unknown magical influence
import encodings.punycode


logger = logging.getLogger('grab.tools.http')
RE_NON_ASCII = re.compile(r'[^-.a-zA-Z0-9]')
RE_NOT_SAFE_URL = re.compile(r'[^-.:/?&;#a-zA-Z0-9]')

# Files content list of top level domains.
# We need to change path variable "PUBLIC_SUFFIX_LIST", otherwise urltools module get it from site.
TLD_FILE_NAME = "effective_tld_names.dat"
path_to_tld = os.path.join(os.path.dirname(os.path.abspath(__file__)), TLD_FILE_NAME)
os.environ['PUBLIC_SUFFIX_LIST'] = path_to_tld

import urltools

#def set_environ():
#    path_to_tld = os.path.join(os.path.dirname(os.path.abspath(__file__)), TLD_FILE_NAME)
#    os.environ['PUBLIC_SUFFIX_LIST'] = path_to_tld

def urlencode(*args, **kwargs):
    logger.debug('Method grab.tools.http.urlencode is deprecated. '
                 'Please use grab.tools.http.smart_urlencode')
    return smart_urlencode(*args, **kwargs)


def smart_urlencode(items, charset='utf-8'):
    """
    Convert sequence of items into bytestring which could be submitted
    in POST or GET request.

    It differs from ``urllib.urlencode`` in that it can process unicode
    and some special values.

    ``items`` could dict or tuple or list.
    """

    if isinstance(items, dict):
        items = items.items()
    return urllib.urlencode(normalize_http_values(items, charset=charset))


def encode_cookies(items, join=True, charset='utf-8'):
    """
    Serialize dict or sequence of two-element items into string suitable
    for sending in Cookie http header.
    """

    def encode(val):
        """
        URL-encode special characters in the text.

        In cookie value only ",", " ", "\t" and ";" should be encoded
        """

        return val.replace(b' ', b'%20').replace(b'\t', b'%09')\
                  .replace(b';', b'%3B').replace(b',', b'%2C')

    if isinstance(items, dict):
        items = items.items()
    items = normalize_http_values(items, charset=charset)

    # py3 hack
    #if PY3K:
    #    items = decode_pairs(items, charset)

    tokens = []
    for key, value in items:
        tokens.append(b'='.join((encode(key), encode(value))))
    if join:
        return b'; '.join(tokens)
    else:
        return tokens


def normalize_http_values(items, charset='utf-8'):
    """
    Accept sequence of (key, value) paris or dict and convert each
    value into bytestring.

    Unicode is converted into bytestring using charset of previous response
    (or utf-8, if no requests were performed)

    None is converted into empty string. 
    """

    if isinstance(items, dict):
        items = items.items()

    def process(item):
        key, value = item

        # normalize value
        if isinstance(value, unicode):
            value = normalize_unicode(value, charset=charset)
        elif value is None:
            value = ''
        else:
            value = str(value)

        # normalize key
        if isinstance(key, unicode):
            key = normalize_unicode(key, charset=charset)

        return key, value

    items =  list(map(process, items))
    #items = sorted(items, key=lambda x: x[0])
    return items


def normalize_unicode(value, charset='utf-8'):
    """
    Convert unicode into byte-string using detected charset (default or from
    previous response)

    By default, charset from previous response is used to encode unicode into
    byte-string but you can enforce charset with ``charset`` option
    """

    if not isinstance(value, unicode):
        return value
    else:
        #raise RuntimeConfigError('normalize_unicode function accepts only unicode values')
        return value.encode(charset, 'ignore')


def quote(data):
    return urllib.quote_plus(smart_str(data))


def normalize_url(url):
    return urltools.encode(url)


def normalize_post_data(data, charset):
    if isinstance(data, basestring):
        # bytes-string should be posted as-is
        # unicode should be converted into byte-string
        if isinstance(data, unicode):
            return normalize_unicode(data, charset)
        else:
            return data
    else:
        # dict, tuple, list should be serialized into byte-string
        return smart_urlencode(data, charset)
