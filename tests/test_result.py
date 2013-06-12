import unittest

response_text_1 = '''<?xml version="1.0" encoding="UTF-8"?>
<DescribeInstancesResponse xmlns="http://ec2.amazonaws.com/doc/2013-02-01/">
    <requestId>e8fa03b0-f3f5-4b56-a15e-8663217d59a5</requestId>
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
</DescribeInstancesResponse>
'''

response_text_2 = '''<?xml version="1.0" encoding="UTF-8"?>
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

json_2 = {'reservationSet': {'item': {'ownerId': '438543334922', 'groupSet': {'item': {'groupName': 'default', 'groupId': 'sg-68d8302c'}}, 'reservationId': 'r-7e1dff26', 'instancesSet': {'item': {'virtualizationType': 'paravirtual', 'blockDeviceMapping': {'item': {'deviceName': '/dev/sda1', 'ebs': {'status': 'attached', 'deleteOnTermination': 'true', 'volumeId': 'vol-6878e348', 'attachTime': '2013-06-12T16:29:56.000Z'}}}, 'instanceType': 't1.micro', 'privateIpAddress': '10.160.185.141', 'rootDeviceType': 'ebs', 'privateDnsName': 'ip-10-160-185-141.us-west-1.compute.internal', 'dnsName': 'ec2-50-18-97-16.us-west-1.compute.amazonaws.com', 'rootDeviceName': '/dev/sda1', 'ebsOptimized': 'false', 'reason': '', 'amiLaunchIndex': '0', 'architecture': 'x86_64', 'groupSet': {'item': {'groupName': 'default', 'groupId': 'sg-68d8302c'}}, 'instanceId': 'i-7dbd5326', 'instanceState': {'code': '16', 'name': 'running'}, 'monitoring': {'state': 'disabled'}, 'imageId': 'ami-d383af96', 'launchTime': '2013-06-12T16:29:53.000Z', 'hypervisor': 'xen', 'kernelId': 'aki-f77e26b2', 'productCodes': '', 'networkInterfaceSet': '', 'clientToken': '', 'placement': {'groupName': '', 'availabilityZone': 'us-west-1a', 'tenancy': 'default'}, 'ipAddress': '50.18.97.16'}}}}, 'requestId': '37f3ddab-ab6b-4968-a4e5-80277b8afbaa'}

class TestAWSResult(unittest.TestCase):
    maxDiff = None
    def test_parse_json(self):
        from faws.result import AWSResult
        result = AWSResult(response_text_2)
        json = result.json()
        self.assertEqual(json_2, json)
