import unittest

class TestAWSResult(unittest.TestCase):
    maxDiff = None
    def test_parse_json(self):
        from faws.result import AWSResult

        result = AWSResult(response_text_2)
        self.assertEqual(response_json_full_2, result.json_full())
#        self.assertEqual(response_json_2, result.json())
        
        result = AWSResult(response_text_1)
        self.assertEqual(response_json_full_1, result.json_full())
#        self.assertEqual(response_json_1, result.json())

response_text_1 = '''<?xml version="1.0" encoding="UTF-8"?>
<DescribeInstancesResponse xmlns="http://ec2.amazonaws.com/doc/2013-02-01/">
    <requestId>37f3ddab-ab6b-4968-a4e5-80277b8afbaa</requestId>
    <reservationSet>
        <item>
            <reservationId>r-7e1dff26</reservationId>
            <ownerId>438543334922</ownerId>
            <groupSet>
                <item>
                    <groupId>sg-68d8302c</groupId>
                    <groupName>default</groupName>
                </item>
            </groupSet>
            <instancesSet>
                <item>
                    <instanceId>i-7dbd5326</instanceId>
                    <imageId>ami-d383af96</imageId>
                    <instanceState>
                        <code>16</code>
                        <name>running</name>
                    </instanceState>
                    <privateDnsName>ip-10-160-185-141.us-west-1.compute.internal</privateDnsName>
                    <dnsName>ec2-50-18-97-16.us-west-1.compute.amazonaws.com</dnsName>
                    <reason/>
                    <amiLaunchIndex>0</amiLaunchIndex>
                    <productCodes/>
                    <instanceType>t1.micro</instanceType>
                    <launchTime>2013-06-12T16:29:53.000Z</launchTime>
                    <placement>
                        <availabilityZone>us-west-1a</availabilityZone>
                        <groupName/>
                        <tenancy>default</tenancy>
                    </placement>
                    <kernelId>aki-f77e26b2</kernelId>
                    <monitoring>
                        <state>disabled</state>
                    </monitoring>
                    <privateIpAddress>10.160.185.141</privateIpAddress>
                    <ipAddress>50.18.97.16</ipAddress>
                    <groupSet>
                        <item>
                            <groupId>sg-68d8302c</groupId>
                            <groupName>default</groupName>
                        </item>
                    </groupSet>
                    <architecture>x86_64</architecture>
                    <rootDeviceType>ebs</rootDeviceType>
                    <rootDeviceName>/dev/sda1</rootDeviceName>
                    <blockDeviceMapping>
                        <item>
                            <deviceName>/dev/sda1</deviceName>
                            <ebs>
                                <volumeId>vol-6878e348</volumeId>
                                <status>attached</status>
                                <attachTime>2013-06-12T16:29:56.000Z</attachTime>
                                <deleteOnTermination>true</deleteOnTermination>
                            </ebs>
                        </item>
                    </blockDeviceMapping>
                    <virtualizationType>paravirtual</virtualizationType>
                    <clientToken/>
                    <hypervisor>xen</hypervisor>
                    <networkInterfaceSet/>
                    <ebsOptimized>false</ebsOptimized>
                </item>
            </instancesSet>
        </item>
    </reservationSet>
</DescribeInstancesResponse>'''

response_json_full_1 = {'reservationSet': {'item': {'ownerId': '438543334922', 'groupSet': {'item': {'groupName': 'default', 'groupId': 'sg-68d8302c'}}, 'reservationId': 'r-7e1dff26', 'instancesSet': {'item': {'virtualizationType': 'paravirtual', 'blockDeviceMapping': {'item': {'deviceName': '/dev/sda1', 'ebs': {'status': 'attached', 'deleteOnTermination': 'true', 'volumeId': 'vol-6878e348', 'attachTime': '2013-06-12T16:29:56.000Z'}}}, 'instanceType': 't1.micro', 'privateIpAddress': '10.160.185.141', 'rootDeviceType': 'ebs', 'privateDnsName': 'ip-10-160-185-141.us-west-1.compute.internal', 'dnsName': 'ec2-50-18-97-16.us-west-1.compute.amazonaws.com', 'rootDeviceName': '/dev/sda1', 'ebsOptimized': 'false', 'reason': '', 'amiLaunchIndex': '0', 'architecture': 'x86_64', 'groupSet': {'item': {'groupName': 'default', 'groupId': 'sg-68d8302c'}}, 'instanceId': 'i-7dbd5326', 'instanceState': {'code': '16', 'name': 'running'}, 'monitoring': {'state': 'disabled'}, 'imageId': 'ami-d383af96', 'launchTime': '2013-06-12T16:29:53.000Z', 'hypervisor': 'xen', 'kernelId': 'aki-f77e26b2', 'productCodes': '', 'networkInterfaceSet': '', 'clientToken': '', 'placement': {'groupName': '', 'availabilityZone': 'us-west-1a', 'tenancy': 'default'}, 'ipAddress': '50.18.97.16'}}}}, 'requestId': '37f3ddab-ab6b-4968-a4e5-80277b8afbaa'}

response_json_1 = {
    'requestId': 'c2638b7c-a2e3-480f-97e7-2cb3259ad656',
    'reservations': [
        {'groups':
             [{'groupId': 'sg-68d8302c', 'groupName': 'default'}],
         'instances': [
                {'amiLaunchIndex': '0',
                 'architecture': 'x86_64',
                 'blockDeviceMapping': {'item': {'deviceName': '/dev/sda1',
                                                 'ebs': {'attachTime': '2013-06-12T16:29:56.000Z',
                                                         'deleteOnTermination': 'true',
                                                         'status': 'attached',
                                                         'volumeId': 'vol-6878e348'}}},
                 'clientToken': '',
                 'dnsName': 'ec2-50-18-97-16.us-west-1.compute.amazonaws.com',
                 'ebsOptimized': 'false',
                 'groupSet': {'item': {'groupId': 'sg-68d8302c',
                                       'groupName': 'default'}},
                 'hypervisor': 'xen',
                 'imageId': 'ami-d383af96',
                 'instanceId': 'i-7dbd5326',
                 'instanceState': {'code': '16',
                                   'name': 'running'},
                 'instanceType': 't1.micro',
                 'ipAddress': '50.18.97.16',
                 'kernelId': 'aki-f77e26b2',
                 'launchTime': '2013-06-12T16:29:53.000Z',
                 'monitoring': {'state': 'disabled'},
                 'networkInterfaceSet': '',
                 'placement': {'availabilityZone': 'us-west-1a',
                               'groupName': '',
                               'tenancy': 'default'},
                 'privateDnsName': 'ip-10-160-185-141.us-west-1.compute.internal',
                 'privateIpAddress': '10.160.185.141',
                 'productCodes': '',
                 'reason': '',
                 'rootDeviceName': '/dev/sda1',
                 'rootDeviceType': 'ebs',
                 'virtualizationType': 'paravirtual'}],
         'ownerId': '438543334922',
         'reservationId': 'r-7e1dff26'}
        ]
    }


response_text_2 = '''<DescribeInstancesResponse>
    <requestId>29f33462-f83c-4f3f-ad00-b135ae7f1e83</requestId>
    <reservationSet>
        <item>
            <reservationId>r-7e1dff26</reservationId>
            <ownerId>438543334922</ownerId>
            <groupSet>
                <item>
                    <groupId>sg-68d8302c</groupId>
                    <groupName>default</groupName>
                </item>
            </groupSet>
            <instancesSet>
                <item>
                    <instanceId>i-7dbd5326</instanceId>
                    <imageId>ami-d383af96</imageId>
                    <instanceState>
                        <code>16</code>
                        <name>running</name>
                    </instanceState>
                    <privateDnsName>ip-10-160-185-141.us-west-1.compute.internal</privateDnsName>
                    <dnsName>ec2-50-18-97-16.us-west-1.compute.amazonaws.com</dnsName>
                    <reason/>
                    <amiLaunchIndex>0</amiLaunchIndex>
                    <productCodes/>
                    <instanceType>t1.micro</instanceType>
                    <launchTime>2013-06-12T16:29:53.000Z</launchTime>
                    <placement>
                        <availabilityZone>us-west-1a</availabilityZone>
                        <groupName/>
                        <tenancy>default</tenancy>
                    </placement>
                    <kernelId>aki-f77e26b2</kernelId>
                    <monitoring>
                        <state>disabled</state>
                    </monitoring>
                    <privateIpAddress>10.160.185.141</privateIpAddress>
                    <ipAddress>50.18.97.16</ipAddress>
                    <groupSet>
                        <item>
                            <groupId>sg-68d8302c</groupId>
                            <groupName>default</groupName>
                        </item>
                    </groupSet>
                    <architecture>x86_64</architecture>
                    <rootDeviceType>ebs</rootDeviceType>
                    <rootDeviceName>/dev/sda1</rootDeviceName>
                    <blockDeviceMapping>
                        <item>
                            <deviceName>/dev/sda1</deviceName>
                            <ebs>
                                <volumeId>vol-6878e348</volumeId>
                                <status>attached</status>
                                <attachTime>2013-06-12T16:29:56.000Z</attachTime>
                                <deleteOnTermination>true</deleteOnTermination>
                            </ebs>
                        </item>
                    </blockDeviceMapping>
                    <virtualizationType>paravirtual</virtualizationType>
                    <clientToken/>
                    <hypervisor>xen</hypervisor>
                    <networkInterfaceSet/>
                    <ebsOptimized>false</ebsOptimized>
                </item>
            </instancesSet>
        </item>
        <item>
            <reservationId>r-2c4daf74</reservationId>
            <ownerId>438543334922</ownerId>
            <groupSet>
                <item>
                    <groupId>sg-68d8302c</groupId>
                    <groupName>default</groupName>
                </item>
            </groupSet>
            <instancesSet>
                <item>
                    <instanceId>i-35fb156e</instanceId>
                    <imageId>ami-d383af96</imageId>
                    <instanceState>
                        <code>16</code>
                        <name>running</name>
                    </instanceState>
                    <privateDnsName>ip-10-176-45-93.us-west-1.compute.internal</privateDnsName>
                    <dnsName>ec2-184-169-202-216.us-west-1.compute.amazonaws.com</dnsName>
                    <reason/>
                    <amiLaunchIndex>0</amiLaunchIndex>
                    <productCodes/>
                    <instanceType>t1.micro</instanceType>
                    <launchTime>2013-06-12T18:46:25.000Z</launchTime>
                    <placement>
                        <availabilityZone>us-west-1a</availabilityZone>
                        <groupName/>
                        <tenancy>default</tenancy>
                    </placement>
                    <kernelId>aki-f77e26b2</kernelId>
                    <monitoring>
                        <state>disabled</state>
                    </monitoring>
                    <privateIpAddress>10.176.45.93</privateIpAddress>
                    <ipAddress>184.169.202.216</ipAddress>
                    <groupSet>
                        <item>
                            <groupId>sg-68d8302c</groupId>
                            <groupName>default</groupName>
                        </item>
                    </groupSet>
                    <architecture>x86_64</architecture>
                    <rootDeviceType>ebs</rootDeviceType>
                    <rootDeviceName>/dev/sda1</rootDeviceName>
                    <blockDeviceMapping>
                        <item>
                            <deviceName>/dev/sda1</deviceName>
                            <ebs>
                                <volumeId>vol-820299a2</volumeId>
                                <status>attached</status>
                                <attachTime>2013-06-12T18:46:31.000Z</attachTime>
                                <deleteOnTermination>true</deleteOnTermination>
                            </ebs>
                        </item>
                    </blockDeviceMapping>
                    <virtualizationType>paravirtual</virtualizationType>
                    <clientToken/>
                    <hypervisor>xen</hypervisor>
                    <networkInterfaceSet/>
                    <ebsOptimized>false</ebsOptimized>
                </item>
            </instancesSet>
        </item>
        <item>
            <reservationId>r-7252b02a</reservationId>
            <ownerId>438543334922</ownerId>
            <groupSet>
                <item>
                    <groupId>sg-68d8302c</groupId>
                    <groupName>default</groupName>
                </item>
            </groupSet>
            <instancesSet>
                <item>
                    <instanceId>i-01f8165a</instanceId>
                    <imageId>ami-d383af96</imageId>
                    <instanceState>
                        <code>16</code>
                        <name>running</name>
                    </instanceState>
                    <privateDnsName>ip-10-160-186-101.us-west-1.compute.internal</privateDnsName>
                    <dnsName>ec2-204-236-189-245.us-west-1.compute.amazonaws.com</dnsName>
                    <reason/>
                    <amiLaunchIndex>0</amiLaunchIndex>
                    <productCodes/>
                    <instanceType>t1.micro</instanceType>
                    <launchTime>2013-06-12T18:48:53.000Z</launchTime>
                    <placement>
                        <availabilityZone>us-west-1a</availabilityZone>
                        <groupName/>
                        <tenancy>default</tenancy>
                    </placement>
                    <kernelId>aki-f77e26b2</kernelId>
                    <monitoring>
                        <state>disabled</state>
                    </monitoring>
                    <privateIpAddress>10.160.186.101</privateIpAddress>
                    <ipAddress>204.236.189.245</ipAddress>
                    <groupSet>
                        <item>
                            <groupId>sg-68d8302c</groupId>
                            <groupName>default</groupName>
                        </item>
                    </groupSet>
                    <architecture>x86_64</architecture>
                    <rootDeviceType>ebs</rootDeviceType>
                    <rootDeviceName>/dev/sda1</rootDeviceName>
                    <blockDeviceMapping>
                        <item>
                            <deviceName>/dev/sda1</deviceName>
                            <ebs>
                                <volumeId>vol-b5019a95</volumeId>
                                <status>attached</status>
                                <attachTime>2013-06-12T18:48:58.000Z</attachTime>
                                <deleteOnTermination>true</deleteOnTermination>
                            </ebs>
                        </item>
                    </blockDeviceMapping>
                    <virtualizationType>paravirtual</virtualizationType>
                    <clientToken/>
                    <hypervisor>xen</hypervisor>
                    <networkInterfaceSet/>
                    <ebsOptimized>false</ebsOptimized>
                </item>
            </instancesSet>
        </item>
    </reservationSet>
</DescribeInstancesResponse>'''

response_json_full_2 = {
    'requestId': '29f33462-f83c-4f3f-ad00-b135ae7f1e83',
    'reservationSet': {'item': [{'groupSet': {'item': {'groupId': 'sg-68d8302c',
                                                       'groupName': 'default'}},
                                 'instancesSet': {'item': {'amiLaunchIndex': '0',
                                                           'architecture': 'x86_64',
                                                           'blockDeviceMapping': {'item': {'deviceName': '/dev/sda1',
                                                                                           'ebs': {'attachTime': '2013-06-12T16:29:56.000Z',
                                                                                                   'deleteOnTermination': 'true',
                                                                                                   'status': 'attached',
                                                                                                   'volumeId': 'vol-6878e348'}}},
                                                           'clientToken': '',
                                                           'dnsName': 'ec2-50-18-97-16.us-west-1.compute.amazonaws.com',
                                                           'ebsOptimized': 'false',
                                                           'groupSet': {'item': {'groupId': 'sg-68d8302c',
                                                                                 'groupName': 'default'}},
                                                           'hypervisor': 'xen',
                                                           'imageId': 'ami-d383af96',
                                                           'instanceId': 'i-7dbd5326',
                                                           'instanceState': {'code': '16',
                                                                             'name': 'running'},
                                                           'instanceType': 't1.micro',
                                                           'ipAddress': '50.18.97.16',
                                                           'kernelId': 'aki-f77e26b2',
                                                           'launchTime': '2013-06-12T16:29:53.000Z',
                                                           'monitoring': {'state': 'disabled'},
                                                           'networkInterfaceSet': '',
                                                           'placement': {'availabilityZone': 'us-west-1a',
                                                                         'groupName': '',
                                                                         'tenancy': 'default'},
                                                           'privateDnsName': 'ip-10-160-185-141.us-west-1.compute.internal',
                                                           'privateIpAddress': '10.160.185.141',
                                                           'productCodes': '',
                                                           'reason': '',
                                                           'rootDeviceName': '/dev/sda1',
                                                           'rootDeviceType': 'ebs',
                                                           'virtualizationType': 'paravirtual'}},
                                 'ownerId': '438543334922',
                                 'reservationId': 'r-7e1dff26'},
                                {'groupSet': {'item': {'groupId': 'sg-68d8302c',
                                                       'groupName': 'default'}},
                                 'instancesSet': {'item': {'amiLaunchIndex': '0',
                                                           'architecture': 'x86_64',
                                                           'blockDeviceMapping': {'item': {'deviceName': '/dev/sda1',
                                                                                           'ebs': {'attachTime': '2013-06-12T18:46:31.000Z',
                                                                                                   'deleteOnTermination': 'true',
                                                                                                   'status': 'attached',
                                                                                                   'volumeId': 'vol-820299a2'}}},
                                                           'clientToken': '',
                                                           'dnsName': 'ec2-184-169-202-216.us-west-1.compute.amazonaws.com',
                                                           'ebsOptimized': 'false',
                                                           'groupSet': {'item': {'groupId': 'sg-68d8302c',
                                                                                 'groupName': 'default'}},
                                                           'hypervisor': 'xen',
                                                           'imageId': 'ami-d383af96',
                                                           'instanceId': 'i-35fb156e',
                                                           'instanceState': {'code': '16',
                                                                             'name': 'running'},
                                                           'instanceType': 't1.micro',
                                                           'ipAddress': '184.169.202.216',
                                                           'kernelId': 'aki-f77e26b2',
                                                           'launchTime': '2013-06-12T18:46:25.000Z',
                                                           'monitoring': {'state': 'disabled'},
                                                           'networkInterfaceSet': '',
                                                           'placement': {'availabilityZone': 'us-west-1a',
                                                                         'groupName': '',
                                                                         'tenancy': 'default'},
                                                           'privateDnsName': 'ip-10-176-45-93.us-west-1.compute.internal',
                                                           'privateIpAddress': '10.176.45.93',
                                                           'productCodes': '',
                                                           'reason': '',
                                                           'rootDeviceName': '/dev/sda1',
                                                           'rootDeviceType': 'ebs',
                                                           'virtualizationType': 'paravirtual'}},
                                 'ownerId': '438543334922',
                                 'reservationId': 'r-2c4daf74'},
                                {'groupSet': {'item': {'groupId': 'sg-68d8302c',
                                                       'groupName': 'default'}},
                                 'instancesSet': {'item': {'amiLaunchIndex': '0',
                                                           'architecture': 'x86_64',
                                                           'blockDeviceMapping': {'item': {'deviceName': '/dev/sda1',
                                                                                           'ebs': {'attachTime': '2013-06-12T18:48:58.000Z',
                                                                                                   'deleteOnTermination': 'true',
                                                                                                   'status': 'attached',
                                                                                                   'volumeId': 'vol-b5019a95'}}},
                                                           'clientToken': '',
                                                           'dnsName': 'ec2-204-236-189-245.us-west-1.compute.amazonaws.com',
                                                           'ebsOptimized': 'false',
                                                           'groupSet': {'item': {'groupId': 'sg-68d8302c',
                                                                                 'groupName': 'default'}},
                                                           'hypervisor': 'xen',
                                                           'imageId': 'ami-d383af96',
                                                           'instanceId': 'i-01f8165a',
                                                           'instanceState': {'code': '16',
                                                                             'name': 'running'},
                                                           'instanceType': 't1.micro',
                                                           'ipAddress': '204.236.189.245',
                                                           'kernelId': 'aki-f77e26b2',
                                                           'launchTime': '2013-06-12T18:48:53.000Z',
                                                           'monitoring': {'state': 'disabled'},
                                                           'networkInterfaceSet': '',
                                                           'placement': {'availabilityZone': 'us-west-1a',
                                                                         'groupName': '',
                                                                         'tenancy': 'default'},
                                                           'privateDnsName': 'ip-10-160-186-101.us-west-1.compute.internal',
                                                           'privateIpAddress': '10.160.186.101',
                                                           'productCodes': '',
                                                           'reason': '',
                                                           'rootDeviceName': '/dev/sda1',
                                                           'rootDeviceType': 'ebs',
                                                           'virtualizationType': 'paravirtual'}},
                                 'ownerId': '438543334922',
                                 'reservationId': 'r-7252b02a'}]}}
