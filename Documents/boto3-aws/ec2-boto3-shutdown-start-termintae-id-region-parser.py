from sys import argv
import boto3, sys


def Running_instances(region, action):
    """
    return a list Ec2 Instance with the status running or pending.
    """
    ec2 = boto3.resource('ec2', region_name=region)
    
    if action == 'shutdown':
        filter = [{'Name': 'instance-state-name', 'Values': ['pending', 'running',]},]
    if action == 'start':
        filter = [{'Name': 'instance-state-name', 'Values': ['stopped',]},]
    
    instances = ec2.instances.filter(Filters=filter) 
    return [instance.id for instance in instances]
    

def action_ec2_instances(ids,action, region='us-east-2'):
    """
    stop the instance in the list ids
    """
    ec2 = boto3.client('ec2', region_name=region)
    
    if not ids:
        print("No Instances found to {}".format(action))
    else:
        if action == 'shutdown':
            ec2.stop_instances(InstanceIds=ids)
            ec2.get_waiter('instance_stopped').wait(InstanceIds=ids)
        if action == 'start':
            ec2.start_instances(InstanceIds=ids)
            ec2.get_waiter('instance_running').wait(InstanceIds=ids)
        if action == 'terminate':
            ec2.terminate_intances(InstanceIds=ids)
            ec2.get_waiter('instance_terminated').wait(InstanceIds=ids)
        print('instances {} : {}'.format(ids, action))

if __name__ == "__main__":
    """
    shuting down ec2 instances in a specific regions : "ec2-boto3-shutdown.py -r region --id id...."
    ex : python ec2-boto3-shutdown.py -region 'us-east-2' --id 'i-066f53451ca1318ba'
    """
    import argparse
    parser = argparse.ArgumentParser(description='action Ec2 Instances')
    parser.add_argument('-r', '-region', help='the region of the EC2 Instance? ex : us-east-1, eu-west-3, ...', default=True, dest='region')
    parser.add_argument('-a', '-action', help='choose wish action to perform: shutdown, terminate, start', default=True, dest='action')
    parser.add_argument('--id', '--instanceid', help='id of instance', default=False, dest='id')
    args = parser.parse_args()

if not args.id:
    action_ec2_instances(ids=Running_instances(region=args.region, action=args.action),action=args.action, region=args.region)
else:
    action_ec2_instances(ids=[args.id], action=args.action, region=args.region)