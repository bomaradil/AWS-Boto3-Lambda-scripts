from sys import argv
import boto3, sys

"""
shuting down ec2 instances in a specific regions : "ec2-boto3-shutdown.py region-1 region-2 ...."
ex : python ec2-boto3-shutdown.py us-east-1 eu-west-3
"""

def Running_instances(region):
    """
    return a list Ec2 Instance with the status running or pending.
    """
    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['pending', 'running',]},]) 
    return [instance.id for instance in instances]
    

def stop_running_instances(ids=[], region='us-east-2'):
    """
    stop the instance in the list ids
    """
    ec2 = boto3.client('ec2', region_name=region)
    
    if not ids:
        print("No Instance in the state Running or pending")
    else:
        ec2.stop_instances(InstanceIds=ids)
        ec2.get_waiter('instance_stopped').wait(InstanceIds=ids)
        print('instances {} were shutdown'.format(ids))

for region in sys.argv[1:]:
    stop_running_instances(ids=Running_instances(region=region), region=region)

