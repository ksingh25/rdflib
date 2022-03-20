"""Open an arbitrary URL.

Adapted for Micropython by Alex Cowan <acowan@gmail.com>

Works in a similar way to python-requests http://docs.python-requests.org/en/latest/
"""

import socket
try:
    import ussl as ssl
except:
    import ssl
import binascii
from urllib.parse import *
import re

class URLOpener:
    def __init__(self, url, method, params = {}, data = {}, headers = {}, cookies = {}, auth = (), timeout = 5):
        self.status_code = 0
        self.headers = {}
        self.text = ""
        self.url = url ##cast it as string??
        [scheme, host, port, path, query_string] = urlparse(self.url)
        if auth and isinstance(auth, tuple) and len(auth) == 2:
            headers['Authorization'] = 'Basic %s' % (b64encode('%s:%s' % (auth[0], auth[1])))
        if scheme == 'http':
            addr = socket.getaddrinfo(host, int(port))[0][-1]
            s = socket.socket()
            s.settimeout(5)
            print("try http connection", host, port, socket.inet_ntop(socket.AF_INET, addr)) ##
            s.connect(addr)
        else:
            ##sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SEC)
            sock=socket.socket()
            sock.connect(socket.getaddrinfo(host, port)[0][4])
            sock.settimeout(5)
            s = ssl.wrap_socket(sock)
            ##s.connect(socket.getaddrinfo(host, port)[0][4])
        if params:
            enc_params = urlencode(params)
            path = path + '?' + enc_params.strip()
        header_string = 'Host: %s\r\n' % host
        if headers:
            for k, v in headers.items():
                header_string += '%s: %s\r\n' % (k, v)
        if cookies:
            for k, v in cookies.items():
                header_string += 'Cookie: %s=%s\r\n' % (k, quote_plus(v))
        request = b'%s %s HTTP/1.0\r\n%s' % (method, path, header_string)
        if data:
            if isinstance(data, dict):
                enc_data = urlencode(data)
                if not headers.get('Content-Type'):
                    request += 'Content-Type: application/x-www-form-urlencoded\r\n'
                request += 'Content-Length: %s\r\n\r\n%s\r\n' % (len(enc_data), enc_data)
            else:
                request += 'Content-Length: %s\r\n\r\n%s\r\n' % (len(data), data)
        request += '\r\n'
        s.send(request)
        while 1:
            recv = s.recv(1024)
            if len(recv) == 0: break
            self.text += recv.decode()
        s.close()
        self._parse_result()

    def read(self):
        return self.text

    def _parse_result(self):
        self.text = self.text.split('\r\n')
        while self.text:
            line = self.text.pop(0).strip()
            if line == '':
                 break
            if line[0:4] == 'HTTP':
                data = line.split(' ')
                self.status_code = int(data[1])
                continue
            if len(line.split(':')) >= 2:
                data = line.split(':')
                self.headers[data[0]] = (':'.join(data[1:])).strip()
                continue
        self.text = '\r\n'.join(self.text)
        return
    def geturl(self):
        return self.url

def urlparse(url):
    scheme = url.split('://')[0].lower()
    url = url.split('://')[1]
    host = url.split('/')[0]
    path = '/'
    data = ""
    port = 80
    if scheme == 'https':
        port = 443
    if host != url:
        path = '/'+'/'.join(url.split('/')[1:])
        if path.count('?'):
            if path.count('?') > 1:
                raise Exception('URL malformed, too many ?')
            [path, data] = path.split('?')
    if host.count(':'):
        [host, port] = host.split(':')
    if path[0] != '/':
        path = '/'+path
    return [scheme, host, port, path, data]

def get(url, params={}, **kwargs):
    return urlopen(url, "GET", params = params, **kwargs)

def post(url, data={}, **kwargs):
    return urlopen(url, "POST", data = data, **kwargs)

def put(url, data={}, **kwargs):
    return urlopen(url, "PUT", data = data, **kwargs)

def delete(url, **kwargs):
    return urlopen(url, "DELETE", **kwargs)

def head(url, **kwargs):
    return urlopen(url, "HEAD", **kwargs)

def options(url, **kwargs):
    return urlopen(url, "OPTIONS", **kwargs)

def urlopen(url, method="GET", params = {}, data = {}, headers = {}, cookies = {}, auth = (), timeout = 5, **kwargs):
    orig_url = url
    attempts = 0
    result = URLOpener(url, method, params, data, headers, cookies, auth, timeout)
    ## Maximum of 4 redirects
    while attempts < 4:
        attempts += 1
        if result.status_code in (301, 302):
            url = result.headers.get('Location', '')
            if not url.count('://'):
                [scheme, host, path, data] = urlparse(orig_url)
                url = '%s://%s%s' % (scheme, host, url)
            if url:
                result = URLOpener(url)
            else:
                raise Exception('URL returned a redirect but one was not found')
        else:
            return result
    return result

always_safe = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
               'abcdefghijklmnopqrstuvwxyz'
               '0123456789' '_.-')

def quote(s):
    res = []
    replacements = {}
    for c in s:
        if c in always_safe:
            res.append(c)
            continue
        res.append('%%%x' % ord(c))
    return ''.join(res)

def quote_plus(s):
    if ' ' in s:
        s = s.replace(' ', '+')
    return quote(s)

def unquote(s):
    """Kindly rewritten by Damien from Micropython"""
    """No longer uses caching because of memory limitations"""
    res = s.split('%')
    for i in range(1, len(res)):
        item = res[i]
        try:
            res[i] = chr(int(item[:2], 16)) + item[2:]
        except ValueError:
            res[i] = '%' + item
    return "".join(res)

def unquote_plus(s):
    """unquote('%7e/abc+def') -> '~/abc def'"""
    s = s.replace('+', ' ')
    return unquote(s)

def urlencode(query):
    if isinstance(query, dict):
        query = query.items()
    l = []
    for k, v in query:
        if not isinstance(v, list):
            v = [v]
        for value in v:
            k = quote_plus(str(k))
            v = quote_plus(str(value))
            l.append(k + '=' + v)
    return '&'.join(l)

def b64encode(s, altchars=None):
    """Reproduced from micropython base64"""
    if not isinstance(s, (bytes, bytearray)):
        raise TypeError("expected bytes, not %s" % s.__class__.__name__)
    # Strip off the trailing newline
    encoded = binascii.b2a_base64(s)[:-1]
    if altchars is not None:
        if not isinstance(altchars, bytes_types):
            raise TypeError("expected bytes, not %s"
                            % altchars.__class__.__name__)
        assert len(altchars) == 2, repr(altchars)
        return encoded.translate(bytes.maketrans(b'+/', altchars))
    return encoded

_cut_port_re = re.compile(r":\d+$")##, re.ASCII)
##FIXME

def request_host(request):
    """Return request-host, as defined by RFC 2965.
    Variation from RFC: returned value is lowercased, for convenient
    comparison.
    """
    url = request.full_url
    host = urlparse(url)[1]
    if host == "":
        host = request.get_header("Host", "")

    # remove port, if present
    ##host = _cut_port_re.sub("", host, 1)
    ##host = re.sub(_cut_port_re, host, 1)
    ##FIXME on some versions re.sub doesnt exist
    port = re.search(':\d+$', host)
    if (port):
        port = str(port.group(0))
    else:
        port = ""
    host = host.replace(port, "")
  
    return host.lower()

class Request:

    def __init__(self, url, data=None, headers={},
                 origin_req_host=None, unverifiable=False,
                 method=None):
        self.full_url = url##._value
        self.headers = {}
        self.unredirected_hdrs = {}
        self._data = None
        self.data = data
        self._tunnel_host = None
        for key, value in headers.items():
            self.add_header(key, value)
        if origin_req_host is None:
            origin_req_host = request_host(self)
        self.origin_req_host = origin_req_host
        self.unverifiable = unverifiable
        if method:
            self.method = method

    @property
    def full_url(self):
        if self.fragment:
            return '{}#{}'.format(self._full_url, self.fragment)
        return self._full_url

    @full_url.setter
    def full_url(self, url):
        # unwrap('<URL:type://host/path>') --> 'type://host/path'
        self._full_url = unwrap(url)
        self._full_url, self.fragment = splittag(self._full_url)
        self._parse()

    @full_url.deleter
    def full_url(self):
        self._full_url = None
        self.fragment = None
        self.selector = ''

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if data != self._data:
            self._data = data
            # issue 16464
            # if we change data we need to remove content-length header
            # (cause it's most probably calculated for previous value)
            if self.has_header("Content-length"):
                self.remove_header("Content-length")

    @data.deleter
    def data(self):
        self.data = None

    def _parse(self):
        self.type, rest = splittype(self._full_url)
        if self.type is None:
            print(url)
            raise ValueError("unknown url type: %r" % self.full_url)
        self.host, self.selector = splithost(rest)
        if self.host:
            self.host = unquote(self.host)

    def get_method(self):
        """Return a string indicating the HTTP request method."""
        default_method = "POST" if self.data is not None else "GET"
        return getattr(self, 'method', default_method)

    def get_full_url(self):
        return self.full_url

    def set_proxy(self, host, type):
        if self.type == 'https' and not self._tunnel_host:
            self._tunnel_host = self.host
        else:
            self.type= type
            self.selector = self.full_url
        self.host = host

    def has_proxy(self):
        return self.selector == self.full_url

    def add_header(self, key, val):
        # useful for something like authentication
        ##self.headers[key.capitalize()] = val
        self.headers[key.upper()] = val

    def add_unredirected_header(self, key, val):
        # will not be added to a redirected request
        ##self.unredirected_hdrs[key.capitalize()] = val
        self.unredirected_hdrs[key.upper()] = val

    def has_header(self, header_name):
        return (header_name in self.headers or
                header_name in self.unredirected_hdrs)

    def get_header(self, header_name, default=None):
        return self.headers.get(
            header_name,
            self.unredirected_hdrs.get(header_name, default))

    def remove_header(self, header_name):
        self.headers.pop(header_name, None)
        self.unredirected_hdrs.pop(header_name, None)

    def header_items(self):
        hdrs = self.unredirected_hdrs.copy()
        hdrs.update(self.headers)
        return list(hdrs.items())

def url2pathname(pathname):
        """OS-specific conversion from a relative URL of the 'file' scheme
        to a file system path; not recommended for general use."""
        return unquote(pathname)

def pathname2url(pathname):
        """OS-specific conversion from a file system path to a relative URL
        of the 'file' scheme; not recommended for general use."""
        return quote(pathname)