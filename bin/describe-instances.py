#!/usr/bin/env python
from faws.util import assert_pyversion
assert_pyversion()

def get_args():
    import argparse
    parser = argparse.ArgumentParser(
        description='Describe EC2 instances',
        epilog='Demo tool that exercises the DescribeInstances AWS API call',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    parser.add_argument('-r', '--region',
                        help='EC2 region')
    return parser.parse_args()

if '__main__' == __name__:
    from faws import Agent
    agent = Agent()
    future = agent.callf('DescribeInstances')
    result = future.result()
    for instance_id in result.tree().iter('instanceId'):
        print(instance_id.text)
