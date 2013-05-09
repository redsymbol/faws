import unittest
from amitools.creds import Creds
TEST_CREDS = Creds(
    'AKIAIOSFODNN7EXAMPLE',
    'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    'us-east-1',
    )

# disabled v2 tests
class TestSignV2(unittest.TestCase):
    maxDiff = None

    def assertUrlEqual(self, url1, url2, *a, **kw):
        from urllib.parse import (
            urlsplit,
            parse_qs,
            )
        purl1 = urlsplit(url1)
        purl2 = urlsplit(url2)
        self.assertSequenceEqual(purl1.scheme, purl2.scheme, *a, **kw)
        self.assertSequenceEqual(purl1.netloc, purl2.netloc, *a, **kw)
        self.assertSequenceEqual(purl1.path, purl2.path, *a, **kw)
        self.assertSequenceEqual(purl1.fragment, purl2.fragment, *a, **kw)
        query1 = parse_qs(purl1.query)
        query2 = parse_qs(purl2.query)
        self.assertDictEqual(query1, query2, *a, **kw)
        
    def test_signed_request(self):
        # taken from http://docs.aws.amazon.com/general/latest/gr/signature-version-2.html
        from urllib.parse import unquote
        from amitools.sign.v2 import signed_request_basic
        method = 'GET'
        url = 'https://elasticmapreduce.amazonaws.com'
        params = {
            'Action' : 'DescribeJobFlows',
            'Version' : '2009-03-31',
            }
        timestamp_val = '2011-10-03T15:19:30'

        expected_string_to_sign_value = '''GET
elasticmapreduce.amazonaws.com
/
AWSAccessKeyId=AKIAIOSFODNN7EXAMPLE&Action=DescribeJobFlows&SignatureMethod=HmacSHA256&SignatureVersion=2&Timestamp=2011-10-03T15%3A19%3A30&Version=2009-03-31'''
        expected_url = 'https://elasticmapreduce.amazonaws.com?AWSAccessKeyId=AKIAIOSFODNN7EXAMPLE&Action=DescribeJobFlows&SignatureMethod=HmacSHA256&SignatureVersion=2&Timestamp=2011-10-03T15%3A19%3A30&Version=2009-03-31&Signature=i91nKc4PWAt0JJIdXwz9HxZCJDdiy6cf%2FMj6vPxyYIs%3D'
        expected_signature = unquote('i91nKc4PWAt0JJIdXwz9HxZCJDdiy6cf%2FMj6vPxyYIs%3D')
        expected_params_nosig = {
            'Action'           : 'DescribeJobFlows',
            'Version'          : '2009-03-31',
            'Timestamp'        : timestamp_val,
            'SignatureMethod'  : 'HmacSHA256',
            'SignatureVersion' : '2',
            'AWSAccessKeyId'   : TEST_CREDS.access_key,
            }
        
        sr = signed_request_basic(method, url, params, TEST_CREDS, timestamp_val)

        sr_params_nosig = dict(sr.aux['sig_params'])
        del sr_params_nosig['Signature']
        
        self.assertDictEqual(expected_params_nosig, sr_params_nosig)
        self.assertSequenceEqual(expected_string_to_sign_value, sr.aux['string_to_sign_value'])
        self.assertSequenceEqual(expected_signature, sr.aux['signature'])
        self.assertUrlEqual(expected_url, sr.url)

    def test_signature(self):
        from urllib.parse import unquote
        from amitools.sign.v2 import signature
        expected_signature = unquote('i91nKc4PWAt0JJIdXwz9HxZCJDdiy6cf%2FMj6vPxyYIs%3D')
        string_to_sign_value = '''GET
elasticmapreduce.amazonaws.com
/
AWSAccessKeyId=AKIAIOSFODNN7EXAMPLE&Action=DescribeJobFlows&SignatureMethod=HmacSHA256&SignatureVersion=2&Timestamp=2011-10-03T15%3A19%3A30&Version=2009-03-31'''
        secret_key = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
        actual_signature = signature(string_to_sign_value, secret_key)
        self.assertSequenceEqual(expected_signature, actual_signature)
        
    def _test_signature_canonical_str(self):
        from amitools.sign.v2 import canonical_str
        method = 'GET'
        endpoint = 'https://elasticmapreduce.amazonaws.com/'
        params = {
            'Action'           : 'DescribeJobFlows',
            'Version'          : '2009-03-31',
            'AWSAccessKeyId'   : 'AKIAIOSFODNN7EXAMPLE',
            'SignatureVersion' : '2',
            'SignatureMethod'  : 'HmacSHA256',
            'Timestamp'        : '2011-10-03T15:19:30',
            }
        expected = '''GET
elasticmapreduce.amazonaws.com
/
AWSAccessKeyId=AKIAIOSFODNN7EXAMPLE&Action=DescribeJobFlows&SignatureMethod=HmacSHA256&SignatureVersion=2&Timestamp=2011-10-03T15%3A19%3A30&Version=2009-03-31'''
        actual = canonical_str(method, endpoint, params)
        self.assertSequenceEqual(expected, actual)
        
    def _test_signature(self):
        from amitools.sign.v2 import signature
        method = 'GET'
        endpoint = 'https://elasticmapreduce.amazonaws.com/'
        params = {
            'Action'           : 'DescribeJobFlows',
            'Version'          : '2009-03-31',
            'AWSAccessKeyId'   : 'AKIAIOSFODNN7EXAMPLE',
#            'AwsSecretAccessKey' : 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
            'SignatureVersion' : '2',
            'SignatureMethod'  : 'HmacSHA256',
            'Timestamp'        : '2011-10-03T15:19:30',
            }
        expected = b'i91nKc4PWAt0JJIdXwz9HxZCJDdiy6cf/Mj6vPxyYIs='
        actual = signature(method, endpoint, params)
        self.assertSequenceEqual(expected, actual)

