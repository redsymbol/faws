class Service:
    name = None
    protocol = 'https'
    method = 'POST'
    version = '2013-02-01'

    def __init__(self, region):
        self.region = region
        
    def endpoint(self):
        return None

class EC2Service(Service):
    name = 'ec2'
    method = 'GET'
    def endpoint(self):
        return '{}://ec2.{}.amazonaws.com/'.format(self.protocol, self.region)

class IAMService(Service):
    name = 'iam'
    def endpoint(self):
        return '{}://{}/'.format(self.protocol, 'iam.amazonaws.com')
    
services = dict(
    (service_class.name, service_class)
    for service_class in {
        EC2Service,
        IAMService,
        })

def get_service(service_name, region):
    return services[service_name](region)
