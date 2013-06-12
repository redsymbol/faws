class CredsException(Exception):
    pass

class Creds:
    def __init__(self, access_key, secret_key, region):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region

    @classmethod
    def discover(cls):
        try:
            creds = cls.from_environ()
        except KeyError:
            if 'AWS_CREDENTIAL_FILE' not in os.environ:
                raise CredsException('You must define credentials and region! See docs for details')
            creds = self.from_file(os.environ['AWS_CREDENTIAL_FILE'])
        return creds

    @classmethod
    def from_environ(cls):
        import os
        access_key = os.environ['AWS_ACCESS_KEY_ID']
        secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
        region = os.environ['AWS_DEFAULT_REGION']
        return cls(access_key, secret_key, region)

    @classmethod
    def from_file(cls, creds_file_path):
        creds_info = dict()
        with open(creds_file_path) as creds_file:
            for line in creds_file.readlines():
                if '=' in line:
                    parts = line.split('=', 2)
                    key = parts[0].strip().lower()
                    value = parts[1].strip()
                    creds_info[key] = value
        required = {
            'aws_access_key_id',
            'aws_secret_access_key',
            'region',
            }
        missing = set()
        for field in required:
            if field not in creds_info:
                missing.add(field)
        if len(missing) > 0:
            msg = 'Missing fields in creds file {}: '.format(creds_file_path)
            msg += ', '.join(sorted(missing))
            raise CredsException(msg)
        return cls(
            creds_info['aws_access_key_id'],
            creds_info['aws_secret_access_key'],
            creds_info['region'],
            )
