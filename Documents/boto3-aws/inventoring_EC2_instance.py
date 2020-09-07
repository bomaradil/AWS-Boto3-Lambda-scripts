#inventory EC2 instance

import boto3

def Get_Ec2_Instance_Info():
    table_data = list()
    ec2 = boto3.resource('ec2')
    keys= ["instance_id", "vpc_id", "subnet_id", "security_groups", "instance_type", 
           "public_ip_addressd", "image_id", "state", "tags"]
    for instance in ec2.instances.all():
        data = dict(zip(keys, [instance.id, instance.vpc_id, instance.subnet_id, instance.security_groups,  
               instance.instance_type, instance.public_ip_address, instance.image.id, instance.state['Name'], instance.tags,] 
               ))
        table_data.append(data)
    return table_data

def Inventory_Ec2_Instance_RDS(table_name='Inventory_Ec2_Instances', table_data=Get_Ec2_Instance_Info()):
    #import logging
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    with table.batch_writer() as writer:
        for item in table_data:
            writer.put_item(Item=item)
        
def Inventory_Ec2_Instance_Xls_S3(s3_name='', table_data=Get_Ec2_Instance_Info()):
    pass

if __name__ == "__main__":
    Inventory_Ec2_Instance_RDS()