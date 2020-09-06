from sys import argv
import boto3, sys


def Running_instances(region):
    """
    return a list Ec2 Instance with the status running or pending.
    """
    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['pending', 'running',]},]) 
    return [instance.id for instance in instances]
    

def stop_running_instances(ids, region='us-east-2'):
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

if __name__ == "__main__":
    """
    shuting down ec2 instances in a specific regions : "ec2-boto3-shutdown.py -r region --id id...."
    ex : python ec2-boto3-shutdown.py -region 'us-east-2' --id 'i-066f53451ca1318ba'
    """
    import argparse
    parser = argparse.ArgumentParser(description='Shutdown Ec2 Instances')
    parser.add_argument('-r', '-region', help='the region of the EC2 Instance? ex : us-east-1, eu-west-3, ...', default=True, dest='region')
    parser.add_argument('--id', '--instanceid', help='id of instances to shutdown', default=False, dest='id')
    args = parser.parse_args()

if not args.id:
    stop_running_instances(ids=Running_instances(region=args.region), region=args.region)
else:
    stop_running_instances(ids=[args.id], region=args.region)