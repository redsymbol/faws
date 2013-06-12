from faws.sign.common import (
    SignedRequestInfo,
    datadict2payload,
    build_url,
    )

DATETIME_F = ''.join([
        # 20110909T233600Z
        '%Y',
        '%m',
        '%d',
        'T',
        '%H',
        '%M',
        '%S',
        'Z',
        ])

DATETIME_HTTP_F = ''.join([
        # Mon, 09 Sep 2011 23:36:00 GMT
        '%a',
        ', ',
        '%d',
        ' ',
        '%b',
        ' ',
        '%Y',
        ' ',
        '%H',
        ':',
        '%M',
        ':',
        '%S',
        ' GMT',
        ])

def trimall(s):
    '''
    Trims spaces from a string in the manner required to create canonical header values in the AWS API

    Specifically:
      - remove leading and trailing spaces
      - convert sequential spaces in the value to a single space
      - But: do not remove extra spaces from any values that are inside quotation marks
     
    '''
    trimmed = ''
    last = None
    in_quote = False
    for c in s.strip():
        if (not in_quote) and ' ' == c and ' ' == last:
            continue
        if '"' == c and '\\' != last:
            in_quote = not in_quote
        trimmed += c
        last = c
    return trimmed

def canonical_request_body(method, url, headers, when : 'datetime.datetime'):
    '''
    Get the canonical request, minus the payload line

    The AWS docs define a "canonical request", which includes a
    terminal line with a hex-encoded hashed payload. This function
    calculates the "canonical request body", which we define as
    everything in the canonical request except for this payload line.
    '''
    from urllib.parse import (
        urlparse,
        quote,
        )
    import datetime
    assert method in {'POST', 'GET'}, method
    parsed_url = urlparse(url)
    path = parsed_url.path or '/'
    signed_header = ';'.join(sorted(field.lower() for field in headers.keys()))
    canonical_qs_val = parsed_url.query
    print('xxxx ' + canonical_qs_val)
    print('xxxx ' + url)
    cr = '\n'.join([
            method,
            path,
            canonical_qs_val,
            canonical_headers(headers),
            signed_header,
            ])
    return cr

# def _canonical_request(method, url, query, headers, when):
#     payload = ''
#     return canonical_request_body(method, url, headers, when) + '\n' + hexhash(payload)

def hexhash(s):
    '''
    Implements HexEncode(Hash(s)) as defined in the AWS docs
    '''
    import hashlib
    h = hashlib.sha256()
    h.update(s.encode('utf-8'))
    return h.hexdigest().lower()

def canonical_headers(headers : dict):
    pairs = [field.lower() + ':' + trimall(value)
             for field, value in headers.items()]
    return '\n'.join(sorted(pairs)) + '\n'

def datefmt(dt : 'datetime.datetime'):
    '''
    Format the date (year/month/day) only
    '''
    return '{:04d}{:02d}{:02d}'.format(dt.year, dt.month, dt.day)

def datetimefmt(dt : 'datetime.datetime'):
    '''
    Format the date and time
    '''
    return dt.strftime(DATETIME_F)

def credential_scope(region, service_name, when):
    return ''.join([
            datefmt(when),
            '/',
            region,
            '/',
            service_name,
            '/',
            'aws4_request',
            ])

def string_to_sign(region, service_name, cr_hash_value, when):
    return '\n'.join([
            'AWS4-HMAC-SHA256',
            when.strftime(DATETIME_F),
            credential_scope(region, service_name, when),
            cr_hash_value,
            ])

def hmacdigest(key : bytes, val : str):
    import hashlib
    import hmac
    return hmac.new(
        key,
        val.encode('utf-8'),
        digestmod=hashlib.sha256,
        ).digest()

def _signing_key(secret_key, when, region, service_name):
    '''
    Generates signing key and all intermediate values

    Mainly useful for testing.  Normally use signing_key() instead.
    
    '''
    vals = dict()
    vals['kSecret']  = b'AWS4' + secret_key.encode('utf-8')
    vals['kDate']    = hmacdigest(vals['kSecret'], datefmt(when))
    vals['kRegion']  = hmacdigest(vals['kDate'], region)
    vals['kService'] = hmacdigest(vals['kRegion'], service_name)
    vals['kSigning'] = hmacdigest(vals['kService'], "aws4_request")
    return vals

def signing_key(secret_key, when, region, service_name):
    return _signing_key(secret_key, when, region, service_name)['kSigning']

def signature(derived_signing_key, str_to_sign):
    from binascii import hexlify
    return hexlify(hmacdigest(derived_signing_key, str_to_sign)).decode('utf-8')

def cr_hash(method, url, query, headers, data, when):
    data = data or ''
    cr_body = canonical_request_body(method, url, headers, when)
    cr_value = cr_body + '\n' + hexhash(data)
    cr_hexhash = hexhash(cr_value)
    return cr_hexhash, cr_value

def canonical_qs(params):
    parts = []
    for key, val in params.items():
        key = awsquote(key)
        val = awsquote(val)
        parts.append('{}={}'.format(key, val))
    return '&'.join(sorted(parts))

def authorization_header(auth_params):
    '''
    Construct value of Authorization: header from X-Amz-* params
    '''
    return '{X-Amz-Algorithm} Credential={X-Amz-Credential}, SignedHeaders={X-Amz-SignedHeaders}, Signature={X-Amz-Signature}'.format(**auth_params)
        
def awsquote(s):
    from urllib.parse import quote
    return quote(s, safe='A-Za-z0-9-_.~')
    
def normalize_url(url):
    from urllib.parse import (
        urlparse,
        urlunparse,
        quote,
        unquote,
        )
    parsed = urlparse(url)
    ## Fix path
    path = parsed.path
    # remove //
    while '//' in path:
        path = path.replace('//', '/')
    # remove /./
    while '/./' in path:
        path = path.replace('/./', '/')
    # remove /../
    path_segments = path.split('/')
    while True:
        try:
            idx = path_segments.index('..')
        except ValueError:
            break
        assert idx > 0, url
        path_segments = path_segments[:idx-1] + path_segments[idx+1:]
    path = '/'.join(path_segments)
    if '' == path:
        path = '/'
    assert '//' not in path, url
    ## Fix query params
    from collections import defaultdict
    query_params = defaultdict(list)
    query = parsed.query
    if parsed.query:
        for pair in parsed.query.split('&'):
            if '=' in pair:
                key, value = pair.split('=', 1)
            else:
                key, value = pair, ''
            query_params[key].append(value)
        new_query_pairs = []
        for key in sorted(query_params.keys()):
            for value in sorted(query_params[key]):
                key = awsquote(unquote(key))
                value = awsquote(unquote(value))
                new_query_pairs.append(key + '=' + value)
        query = '&'.join(new_query_pairs)
    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        path,
        parsed.params,
        query,
        parsed.fragment,
        ))

def signed_request(service, params, creds, when=None):
    from urllib.parse import urlparse
    service_name = service.name
    method = service.method
    if 'GET' == method:
        url = build_url(service.endpoint(), params)
        data = None
    else:
        url = service.endpoint()
        data = params
    headers = {
        'Date' : when.strftime(DATETIME_HTTP_F),
        'Host' : urlparse(url).hostname,
        'Content-Type': 'application/json',
        }
    return signed_request_basic(
        method,
        service_name,
        url,
        headers,
        datadict2payload(data),
        creds,
        when,
        )

def signed_request_basic(
    method,
    service_name,
    url,
    headers,
    payload,
    creds,
    when=None,
    ):
    import datetime
    from faws.sign.v4 import datefmt
    from urllib.parse import (
        urlparse,
        quote,
        )
    if when is None:
        when = datetime.datetime.now()
    url = normalize_url(url)
    parsed_url = urlparse(url)
    signed_headers = dict(headers)
    cr_hash_value, cr_value = cr_hash(method, url, parsed_url.query, headers, payload, when)
#    from nose.tools import set_trace
#    set_trace()
    signing_key_value = signing_key(
        creds.secret_key,
        when,
        creds.region,
        service_name,
        )
    string_to_sign_value = string_to_sign(
        creds.region,
        service_name,
        cr_hash_value,
        when,
        )
    auth_params = {
        'X-Amz-SignedHeaders' : ';'.join(sorted(header.lower() for header in signed_headers.keys())),
        'X-Amz-Signature'     : signature(signing_key_value, string_to_sign_value),
        'X-Amz-Algorithm'     : 'AWS4-HMAC-SHA256',
        'X-Amz-Date'          : datetimefmt(when),
        'X-Amz-Credential'    : creds.access_key + '/' + credential_scope(creds.region, service_name, when),
        }
    #signed_url_params = dict(cr_params)
    #signed_url = build_url(url, signed_url_params)
    signed_url = url
    signed_payload = None
    sr_headers = dict(signed_headers)
    sr_headers.update({
            'Authorization' : authorization_header(auth_params),
            })
    # print(string_to_sign_value)
    # import pdb
    # pdb.set_trace()
    aux = {
        'auth' : auth_params,
        'cr_value' : cr_value,
        }
    return SignedRequestInfo(
        headers = sr_headers,
        url = signed_url,
        payload = signed_payload,
        aux = aux,
        )

def canonical_qs(params):
    parts = []
    for key, val in params.items():
        key = awsquote(key)
        val = awsquote(val)
        parts.append('{}={}'.format(key, val))
    return '&'.join(sorted(parts))

