from amitools.sign.common import (
    DATETIME_ISO8601_F,
    SignedRequestInfo,
    datadict2payload,
    build_url,
    )

def signed_request(service, params, creds, when):
    params = dict(params)
    params.update({
            'Version' : service.version,
            })
    timestamp_val = when.strftime(DATETIME_ISO8601_F)
    return signed_request_basic(service.method, service.endpoint(), params, creds, timestamp_val)

def signed_request_basic(method, service_endpoint, params, creds, timestamp_val):
    from urllib.parse import urlparse
    sig_params = dict(params)
    sig_params.update({
#        'Timestamp'        : timestamp_val,
        'SignatureMethod'  : 'HmacSHA256',
        'SignatureVersion' : '2',
        'AWSAccessKeyId'   : creds.access_key,
        })
    parsed_url = urlparse(service_endpoint)
    netloc = parsed_url.hostname.lower()
    if parsed_url.port not in {80, 443, None}:
        netloc += ':' + str(parsed_url.port)
    string_to_sign_value = string_to_sign(method, netloc, parsed_url.path, sig_params)
    sig_params['Signature'] = signature(string_to_sign_value, creds.secret_key)
    url = build_url(service_endpoint, sig_params)
    aux = {
        'string_to_sign_value' : string_to_sign_value,
        'sig_params' : sig_params,
        'signature' : sig_params['Signature'],
        }
    return SignedRequestInfo(
        headers = {},
        url     = url,
        payload = None,
        aux     = aux,
        )

def string_to_sign(method, hostname, url, params):
    from urllib.parse import quote
    url = url or '/'
    query = '&'.join(sorted('{}={}'.format(quote(key), quote(value))
                            for key, value in params.items()))
    return '\n'.join([
            method,
            hostname,
            url,
            query,
            ])
    
def signature(string_to_sign_value, secret_key):
    import base64
    digest = hmacdigest(secret_key, string_to_sign_value)
    return base64.b64encode(digest).decode('utf-8')

def hmacdigest(key : str, val : str):
    import hashlib
    import hmac
    new_hmac = hmac.new(
        key.encode('utf-8'),
        digestmod=hashlib.sha256,
        )
    new_hmac.update(val.encode('utf-8'))
    return new_hmac.digest()

def awshash_bytes(s):
    import hashlib
    h = hashlib.sha256()
    h.update(s)
    return h.hexdigest().upper().encode('utf-8')

### older code
def old_signature(method, endpoint, params):
    '''
    calculate HmacSHA256 sig version 2
    '''
    import base64
    s = canonical_str(method, endpoint, params)
    return base64.b64encode(awshash(s))

def canonical_str(method, endpoint, params):
    assert method in {'GET', 'POST'}, method
    assert 'AwsSecretAccessKey' not in params
    from urllib.parse import (
        urlparse,
        quote,
        )
    parsed = urlparse(endpoint)
    netloc = parsed.hostname.lower()
    if parsed.port not in {80, 443, None}:
        netloc += ':' + str(parsed.port)
    path = parsed.path or '/'
    s = '\n'.join([
            method,
            netloc,
            path,
            ]) + '\n'
    qscomponents = []
    for key in sorted(params.keys()):
        value = quote(params[key], safe='.')
        qscomponents.append('{}={}'.format(key, value))
    s += '&'.join(sorted(qscomponents))
    return s
