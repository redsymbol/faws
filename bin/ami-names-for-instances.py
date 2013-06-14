#!/usr/bin/env python
from faws.util import assert_pyversion
assert_pyversion()

def get_args():
    import argparse
    parser = argparse.ArgumentParser(
        description='List launch AMI for each instance ID',
        epilog='Demo tool that demonstrates concurrent API access',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    parser.add_argument('-r', '--region',
                        help='EC2 region')
    return parser.parse_args()

if '__main__' == __name__:
    from faws import Agent
    agent = Agent()
    instances_f = agent.callf('DescribeInstances')
    images_f = agent.callf('DescribeImages')
    # First make map of the AMIs of each instance
    instances = instances_f.result()
    instance_amis = dict()
    for instance_item in instances.tree().xpath('//instancesSet/item'):
        instance_id = instance_item.find('instanceId').text
        image_id = instance_item.find('imageId').text
        instance_amis[instance_id] = image_id
    # Now get the names of each
    ami_names = dict()
    amis_to_check = set(instance_amis.values())
    images = images_f.result()
    for image_item in images.tree().xpath('//imagesSet/item'):
        if len(amis_to_check) == 0:
            break
        image_id = image_item.find('imageId').text
        if image_id in amis_to_check:
            ami_names[image_id] = image_item.find('name').text
            amis_to_check.remove(image_id)
    # Now cross-reference and report
    print('\t'.join(['instanceId', 'amiName']))
    for instance_id in sorted(instance_amis.keys()):
        image_id = instance_amis[instance_id]
        image_name = ami_names[image_id]
        print('\t'.join([instance_id, image_name]))
