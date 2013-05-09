'''
Tests for Amazon's tests for the the V.4 signing process 

To run these tests:

1. Download the AWS4 test suite. Last known location:
https://awsiammedia.s3.amazonaws.com/public/sample/aws4_testsuite/aws4_testsuite.zip
MD5SUM: d04c41088233d5686e2e80ad69e0103d  aws4_testsuite.zip

2. Unpack, and in the environment, export AWS4_TESTSUITE_HOME to the path containing its files.

3. Run via nose as normal.

'''

import os
assert 'AWS4_TESTSUITE_HOME' in os.environ, 'Must define and export AWS4_TESTSUITE_HOME in environment to run test suite. See module docs for details'
AWS4_TESTSUITE_HOME = os.environ['AWS4_TESTSUITE_HOME']

import unittest
import datetime
from amitools.sign.v4 import (
    signed_request_basic,
    DATETIME_F,
    DATETIME_HTTP_F,
    )

from amitools.creds import Creds
REGION = 'us-east-1'
SERVICE_NAME = 'host'
HOSTNAME = 'host.foo.com'
TEST_CREDS = Creds(
    'AKIDEXAMPLE',
    'wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY',
    REGION,
    )
WHEN = datetime.datetime.strptime('20110909T233600Z', DATETIME_F)
#WHEN_HTTP = WHEN.strftime(DATETIME_HTTP_F)
WHEN_HTTP = 'Mon, 09 Sep 2011 23:36:00 GMT'

class TestAWS4TestSuite(unittest.TestCase):
    maxDiff=None
            
    def run_tc(self, testcase):
        import re
        def filepath(ext):
            foo = testcase + '.'
            foo += ext
            return os.path.join(AWS4_TESTSUITE_HOME, foo)

        with open(filepath('creq')) as creq_f:
            creq_content = creq_f.read()
        with open(filepath('req')) as req_f:
            req_content = req_f.read()
        with open(filepath('authz')) as authz_f:
            authz_content = authz_f.read()

        # Determine method
        req_content_fields = re.match('(?P<method>POST|GET) (?P<path>\S+)', req_content)
        method = req_content_fields.group('method')
        assert method in {'GET', 'POST'}, method
        
        # read POST data, if any...
        payload = None
        if 'POST' == method:
            payload_start = req_content.find('\n\n')
            if payload_start > 0:
                payload = req_content[payload_start + 2:]
            else:
                payload = ''

        # Determine URL
        path = req_content_fields.group('path')
        assert path.startswith('/'), path
        url = 'http://{}{}'.format(HOSTNAME, path)

        # request headers
        from collections import defaultdict
        req_content_lines = req_content.split('\n')
        headers = defaultdict(list)
        for line in req_content_lines[1:]:
            if '' == line:
                break # end of request headers
            key, value = line.split(':', 1)
            key = key.lower().strip()
            value = value.strip()
            headers[key].append(value)
        for key in headers:
            values = headers[key]
            headers[key] = ','.join(sorted(values))

        # determine signature
        match = re.search(r'Signature=([^, ]+)', authz_content)
        assert match is not None
        expected_signature = match.group(1)

        # Now execute test
        sr = signed_request_basic(
            method,
            SERVICE_NAME,
            url,
            headers,
            payload,
            TEST_CREDS,
            WHEN,
            )
        
        ## Canonical Request
        expected_cr_value = creq_content
        actual_cr_value = sr.aux['cr_value']
        self.assertSequenceEqual(expected_cr_value, actual_cr_value)

        ## Signature
        actual_signature = sr.aux['auth']['X-Amz-Signature']
        self.assertEqual(expected_signature, actual_signature)


    def test_get_header_key_duplicate(self):
        self.run_tc('get-header-key-duplicate')

#    TODO: this one only has the .req file, missing others?
#    def test_get_header_value_multiline(self):
#        self.run_tc('get-header-value-multiline')

    def test_get_header_value_order(self):
        self.run_tc('get-header-value-order')

    def test_get_header_value_trim(self):
        self.run_tc('get-header-value-trim')

    def test_get_relative_relative(self):
        self.run_tc('get-relative-relative')

    def test_get_relative(self):
        self.run_tc('get-relative')

    def test_get_slash_dot_slash(self):
        self.run_tc('get-slash-dot-slash')

    def test_get_slashes(self):
        self.run_tc('get-slashes')

    def test_get_slash_pointless_dot(self):
        self.run_tc('get-slash-pointless-dot')

    def test_get_slash(self):
        self.run_tc('get-slash')

    def test_get_space(self):
        self.run_tc('get-space')

    def test_get_unreserved(self):
        self.run_tc('get-unreserved')

    def test_get_utf8(self):
        self.run_tc('get-utf8')

    def test_get_vanilla_empty_query_key(self):
        self.run_tc('get-vanilla-empty-query-key')

    def test_get_vanilla_query_order_key_case(self):
        self.run_tc('get-vanilla-query-order-key-case')

    def test_get_vanilla_query_order_key(self):
        self.run_tc('get-vanilla-query-order-key')

    def test_get_vanilla_query_order_value(self):
        self.run_tc('get-vanilla-query-order-value')

    def test_get_vanilla_query(self):
        self.run_tc('get-vanilla-query')

    def test_get_vanilla_query_unreserved(self):
        self.run_tc('get-vanilla-query-unreserved')

    def test_get_vanilla(self):
        self.run_tc('get-vanilla')

    def test_get_vanilla_ut8_query(self):
        self.run_tc('get-vanilla-ut8-query')

    def test_post_header_key_case(self):
        self.run_tc('post-header-key-case')

    def test_post_header_key_sort(self):
        self.run_tc('post-header-key-sort')

    def test_post_header_value_case(self):
        self.run_tc('post-header-value-case')

    def test_post_vanilla_empty_query_value(self):
        self.run_tc('post-vanilla-empty-query-value')

    # TODO: don't quite understand this test case
    # def test_post_vanilla_query_nonunreserved(self):
    #     self.run_tc('post-vanilla-query-nonunreserved')

    def test_post_vanilla_query(self):
        self.run_tc('post-vanilla-query')

    def test_post_vanilla_query_space(self):
        self.run_tc('post-vanilla-query-space')

    def test_post_vanilla(self):
        self.run_tc('post-vanilla')

    def test_post_x_www_form_urlencoded_parameters(self):
        self.run_tc('post-x-www-form-urlencoded-parameters')

    def test_post_x_www_form_urlencoded(self):
        self.run_tc('post-x-www-form-urlencoded')
