'''
The following tests need to be re-enabled and made passing:
  test_canonical_request_body
  test_payload
  test_signed_request

'''
import unittest
import datetime

from amitools.sign.v4 import DATETIME_F

class TestSignV4(unittest.TestCase):
    maxDiff=None
    def test_trimmed(self):
        from amitools.sign.v4 import trimall
        testdata = [
            ('iam.amazonaws.com',
             'iam.amazonaws.com'),
            ('application/x-www-form-urlencoded; charset=utf-8',
             'application/x-www-form-urlencoded; charset=utf-8'),
            ('    application/x-www-form-urlencoded;    charset=utf-8 ',
             'application/x-www-form-urlencoded; charset=utf-8'),
            ('foo "bar   baz" biff',
             'foo "bar   baz" biff'),
            ('foo "bar   baz" biff "bang buck  " boo',
             'foo "bar   baz" biff "bang buck  " boo'),
            ('  foo   "bar   baz" biff "bang \"whoo moo hoo \" buck  "  boo  ',
             'foo "bar   baz" biff "bang \"whoo moo hoo \" buck  " boo'),
            ('foo bar baz biff',
             'foo bar baz biff'),
            ]
        for ii, td in enumerate(testdata):
            actual = trimall(td[0])
            expected = td[1]
            self.assertSequenceEqual(expected, actual, ii)

    def test_canonical_headers(self):
        from amitools.sign.v4 import canonical_headers
        header_dict = {
            'host'         : 'iam.amazonaws.com',
            'Content-type' : 'application/x-www-form-urlencoded; charset=utf-8',
            'My-header1'   : '    a   b   c ',
            'x-amz-date'   : '20120228T030031Z',
            'My-Header2'   : '    "a   b   c"',
            }
        expected = '''content-type:application/x-www-form-urlencoded; charset=utf-8
host:iam.amazonaws.com
my-header1:a b c
my-header2:"a   b   c"
x-amz-date:20120228T030031Z
'''
        self.assertSequenceEqual(expected, canonical_headers(header_dict))
        
    def _test_canonical_request_body(self):
        from amitools.sign.v4 import canonical_request_body
        # POST form
        method = 'POST'
        url = 'http://iam.amazonaws.com/'
        params = {
            'Action' : 'ListUsers',
            'Version' : '2010-05-08',
            'x-amz-date' : '20110909T233600Z',
            }
        credential = 'AKIAIOSFODNN7EXAMPLE/20110909/us-east-1/iam/aws4_request'
        when = datetime.datetime.strptime('20110909T233600Z', DATETIME_F)
        expected = '''POST
/

action:ListUsers
content-type:application/x-www-form-urlencoded; charset=utf-8
host:iam.amazonaws.com
version:2010-05-08
x-amz-date:20110909T233600Z

action;content-type;host;version;x-amz-date'''
        cr_str = canonical_request_body(method, url, params, when)
        self.assertSequenceEqual(expected, cr_str)

    def test_hexhash(self):
        from amitools.sign.v4 import hexhash
        # test on bare payload
        payload = 'Action=ListUsers&Version=2010-05-08'
        payload_hexhash = 'b6359072c78d70ebee1e81adcbab4f01bf2c23245fa365ef83fe8f1f955085e2'
        self.assertSequenceEqual(payload_hexhash, hexhash(payload))
        # test on whole request
        canonical_request = '''POST
/

content-type:application/x-www-form-urlencoded; charset=utf-8
host:iam.amazonaws.com
x-amz-date:20110909T233600Z

content-type;host;x-amz-date
b6359072c78d70ebee1e81adcbab4f01bf2c23245fa365ef83fe8f1f955085e2'''
        cr_hexhash = '3511de7e95d28ecd39e9513b642aee07e54f4941150d8df8bf94b328ef7e55e2'
        self.assertSequenceEqual(cr_hexhash, hexhash(canonical_request))
        

    # TODO: do I need this test?
    def _test_payload(self):
        from amitools.sign.v4 import payload
        params = {
            'Action' : 'ListUsers',
            'Version' : '2010-05-08',
            }
        expected = 'Action=ListUsers&Version=2010-05-08'
        self.assertSequenceEqual(expected, payload(params))

        self.assertSequenceEqual('', payload({}))

    def test_string_to_sign(self):
        from amitools.sign.v4 import string_to_sign
        when = datetime.datetime.strptime('20110909T233600Z', DATETIME_F)
        region = 'us-east-1'
        service = 'iam'
        cr_hash_value = '3511de7e95d28ecd39e9513b642aee07e54f4941150d8df8bf94b328ef7e55e2'
        expected = '''AWS4-HMAC-SHA256
20110909T233600Z
20110909/us-east-1/iam/aws4_request
3511de7e95d28ecd39e9513b642aee07e54f4941150d8df8bf94b328ef7e55e2'''
        actual = string_to_sign(region, service, cr_hash_value, when)
        self.assertSequenceEqual(expected, actual)

    def test_signing_key_internal(self):
        # test data from http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html
        from amitools.sign.v4 import _signing_key
        secret_key = 'wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY'
        when = datetime.datetime.strptime('20120215T233600Z', DATETIME_F)
        region = 'us-east-1'
        service_name = 'iam'
        expected = {
            'kSecret'  : b'\x41\x57\x53\x34\x77\x4a\x61\x6c\x72\x58\x55\x74\x6e\x46\x45\x4d\x49\x2f\x4b\x37\x4d\x44\x45\x4e\x47\x2b\x62\x50\x78\x52\x66\x69\x43\x59\x45\x58\x41\x4d\x50\x4c\x45\x4b\x45\x59',
            'kDate'    : b'\x96\x9f\xbb\x94\xfe\xb5\x42\xb7\x1e\xde\x6f\x87\xfe\x4d\x5f\xa2\x9c\x78\x93\x42\xb0\xf4\x07\x47\x46\x70\xf0\xc2\x48\x9e\x0a\x0d',
            'kRegion'  : b'\x69\xda\xa0\x20\x9c\xd9\xc5\xff\x5c\x8c\xed\x46\x4a\x69\x6f\xd4\x25\x2e\x98\x14\x30\xb1\x0e\x3d\x3f\xd8\xe2\xf1\x97\xd7\xa7\x0c',
            'kService' : b'\xf7\x2c\xfd\x46\xf2\x6b\xc4\x64\x3f\x06\xa1\x1e\xab\xb6\xc0\xba\x18\x78\x0c\x19\xa8\xda\x0c\x31\xac\xe6\x71\x26\x5e\x3c\x87\xfa',
            'kSigning' : b'\xf4\x78\x0e\x2d\x9f\x65\xfa\x89\x5f\x9c\x67\xb3\x2c\xe1\xba\xf0\xb0\xd8\xa4\x35\x05\xa0\x00\xa1\xa9\xe0\x90\xd4\x14\xdb\x40\x4d',
            }
        actual = _signing_key(secret_key, when, region, service_name)
        self.assertDictEqual(expected, actual)
        
    def test_signing_key(self):
        # from example on http://docs.aws.amazon.com/general/latest/gr/sigv4-calculate-signature.html
        from amitools.sign.v4 import signing_key
        secret_key = 'wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY'
        when = datetime.datetime.strptime('20110909T233600Z', DATETIME_F)
        region = 'us-east-1'
        service = 'iam'
        expected = b'\x98\xf1\xd8\x89\xfe\xc4\xf4B\x1a\xdcR+\xab\x0c\xe1\xf8.i)\xc2b\xed\x15\xe5\xa9L\x90\xef\xd1\xe3\xb0\xe7'
        actual = signing_key(secret_key, when, region, service)
        self.assertEqual(expected, actual)

    def test_signature(self):
        from amitools.sign.v4 import signature
        derived_signing_key = b'\x98\xf1\xd8\x89\xfe\xc4\xf4B\x1a\xdcR+\xab\x0c\xe1\xf8.i)\xc2b\xed\x15\xe5\xa9L\x90\xef\xd1\xe3\xb0\xe7'
        str_to_sign = '''AWS4-HMAC-SHA256
20110909T233600Z
20110909/us-east-1/iam/aws4_request
3511de7e95d28ecd39e9513b642aee07e54f4941150d8df8bf94b328ef7e55e2'''
        expected = 'ced6826de92d2bdeed8f846f0bf508e8559e98e4b0199114b84c54174deb456c'
        actual = signature(derived_signing_key, str_to_sign)
        self.assertSequenceEqual(expected, actual)

    def _test_signed_request(self):
        from amitools.sign.v4 import (
            signed_request,
            SignedRequestInfo,
            )
        from amitools.service import get_service
        from amitools.sign.v4 import DATETIME_F
        from amitools.creds import Creds
        
        # GET request
        method = 'GET'
        url = 'https://iam.amazonaws.com/'
        action = 'ListUsers'
        params = {
            'Version' : '2010-05-08',
            }

        expected = SignedRequestInfo(
            headers = {
                'content-type': 'application/json',
                'host' : 'iam.amazonaws.com',
                },
            url = 'https://iam.amazonaws.com/?Action=ListUsers&Version=2010-05-08&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIDEXAMPLE/20110909/us-east-1/iam/aws4_request&X-Amz-Date=20110909T233600Z&X-Amz-Signature=525d1a96c69b5549dd78dbbec8efe264102288b83ba87b7d58d4b76b71f59fd2&X-Amz-SignedHeaders=content-type;host',
            data = None,
            )
        creds = Creds('AKIDEXAMPLE', 'wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY', 'us-east-1')
        when = datetime.datetime.strptime('20110909T233600Z', DATETIME_F)
        actual = signed_request(method, get_service('iam', None), action, params, creds, when)
        self.assertSequenceEqual(sorted(expected.headers.keys()), sorted(actual.headers.keys()))
        for key in sorted(expected.headers.keys()):
            self.assertSequenceEqual(expected.headers[key], actual.headers[key], key)
        self.assertSequenceEqual(expected.url, actual.url)
        self.assertEqual(expected.data, actual.data)


