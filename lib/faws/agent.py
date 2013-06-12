class Agent:
    api_version = '2013-02-01'
    def __init__(self, creds=None):
        from concurrent.futures import ThreadPoolExecutor
        if creds is None:
            from faws.creds import Creds
            creds = Creds.discover()
        self.creds = creds
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.url = 'https://{}.ec2.amazonaws.com/'.format(self.creds.region)

    def full_params(self, method, action, params, now):
        from faws.sign.v4 import (
            signature,
            cr_hash,
            signing_key,
            string_to_sign,
            )
        expires = now + datetime.timedelta(minutes=10)
        params = dict(params)
        params.update({
                'Action'           : action,
                'Version' : '2013-02-01',
                })
        params['Signature'] = signature(
            signing_key(self.creds.secret_key, now, self.creds.region, 'ec2'),
            string_to_sign(self.creds.region,
                           'ec2',
                           cr_hash(method, self.url, params, now),
                           now))
#        params['AwsSecretAccessKey'] = self.creds.secret_key
        
    def call(self, action, params=None, service_name='ec2', now=None):
        from faws.sign.common import DATETIME_ISO8601_F
        import requests
        import datetime
        from faws.service import get_service
        from faws.sign.v2 import signed_request
        if params is None:
            params = {}
        if now is None:
            now = datetime.datetime.utcnow()
        service = get_service(service_name, self.creds.region)
        expires = now + datetime.timedelta(days=5)
        params.update({
                'Action' : action,
                })
        assert service.method in {'GET', 'POST'}, service.name
        # do_request will be one of requests.get or requests.post
        if 'GET' == service.method:
            do_request = requests.get
        else:
            do_request = requests.put
        sr = signed_request(service, params, self.creds, now)
        import pdb
#        pdb.set_trace()
        def do_call():
            return do_request(
                sr.url,
                data = sr.payload,
                headers = sr.headers,
                )
        return self.executor.submit(do_call)

    def call_v4(self, action, params=None, service_name='ec2', now=None):
        from faws.sign.common import DATETIME_ISO8601_F
        import requests
        import datetime
        from faws.service import get_service
        from faws.sign.v4 import (
            datefmt,
            signed_request,
            )
        if params is None:
            params = {}
        if now is None:
            now = datetime.datetime.now()
        service = get_service(service_name, self.creds.region)
        expires = now + datetime.timedelta(minutes=5)
        params.update({
                'Action' : action,
                'Version' : service.version,
                'AWSAccessKeyId' : self.creds.access_key,
                'Timestamp' : now.strftime(DATETIME_ISO8601_F),
                'Expires' : expires.strftime(DATETIME_ISO8601_F),
                })
        assert service.method in {'GET', 'POST'}, service.name
        # do_request will be one of requests.get or requests.post
        if 'GET' == service.method:
            do_request = requests.get
        else:
            do_request = requests.put
        sr = signed_request(service, params, self.creds, when=now)
        import pdb
#        pdb.set_trace()
        def do_call():
            return do_request(
                sr.url,
                data = sr.payload,
                headers = sr.headers,
                )
        return self.executor.submit(do_call)
