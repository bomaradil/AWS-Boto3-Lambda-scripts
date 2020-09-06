import boto3

def Running_instances():
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['pending', 'running',]},])
    return [instance.id for instance in instances]
    
def stop_running_instances(ids=Running_instances()):
    ec2 = boto3.client('ec2')
    if not ids:
        print("No Instance in the state Running or pending")
    else:
        ec2.stop_instances(InstanceIds=ids)
        ec2.get_waiter('instance_stopped').wait(InstanceIds=ids)
        print('instance {} was shutdown'.format(ids))

def lambda_handler(event, context):
    stop_running_instances()
