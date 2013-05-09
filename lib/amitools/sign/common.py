DATETIME_ISO8601_F = ''.join([
        # YYYY-MM-DDThh:mm:ssZ
        '%Y',
        '-',
        '%m',
        '-',
        '%d',
        'T',
        '%H',
        ':',
        '%M',
        ':',
        '%S',
        'Z',
        ])

from collections import namedtuple
SignedRequestInfo = namedtuple('SignedRequestInfo', 'headers url payload aux')

def build_url(base, query_params):
    '''
    Compose a URL from a base URL and query parameters
    '''
    from urllib.parse import quote
    def quote_value(s):
        return quote(s, safe=';/')
    return base + '?' + '&'.join(
        quote(key) + '=' + quote_value(query_params[key])
        for key in sorted(query_params.keys()))

def datadict2payload(data):
    if data is None:
        return ''
    from urllib.parse import quote
    payload_items = []
    for k in sorted(data.keys()):
        if type(data[k]) in (list, tuple, set):
            vals = [data[k]]
        else:
            vals = sorted(data[k])
        quoted_key = quote(k)
        for val in vals:
            payload_items.append('{}={}'.format(quoted_key, quote(val)))
    return '&'.join(payload_items)
