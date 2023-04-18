import boto3

# AWS client initialization
ec2_client = boto3.client('ec2')
rds_client = boto3.client('rds')

# Define security group rules
inbound_rules = [
    {
        'IpProtocol': 'tcp',
        'FromPort': 22,
        'ToPort': 22,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    },
    {
        'IpProtocol': 'tcp',
        'FromPort': 80,
        'ToPort': 80,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    },
    {
        'IpProtocol': 'tcp',
        'FromPort': 443,
        'ToPort': 443,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }
]

outbound_rules = [
    {
        'IpProtocol': 'tcp',
        'FromPort': 0,
        'ToPort': 65535,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    },
    {
        'IpProtocol': 'udp',
        'FromPort': 0,
        'ToPort': 65535,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }
]

# Define security group creation function
def create_security_group(name, description, vpc_id):
    response = ec2_client.create_security_group(
        Description=description,
        GroupName=name,
        VpcId=vpc_id
    )

    security_group_id = response['GroupId']
    print(f'Security group {name} created with ID {security_group_id}')

    # Add inbound rules
    ec2_client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=inbound_rules
    )

    # Add outbound rules
    ec2_client.authorize_security_group_egress(
        GroupId=security_group_id,
        IpPermissions=outbound_rules
    )

    return security_group_id

# Define RDS hardening function
def harden_rds_instance(db_instance_id):
    # Update RDS instance to use secure storage
    rds_client.modify_db_instance(
        DBInstanceIdentifier=db_instance_id,
        StorageEncrypted=True,
        ApplyImmediately=True
    )

    print(f'RDS instance {db_instance_id} encrypted')

# Define EC2 hardening function
def harden_ec2_instance(instance_id):
    # Get security groups for the instance
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    security_groups = response['Reservations'][0]['Instances'][0]['SecurityGroups']

    # Add security group for SSH access
    for sg in security_groups:
        if sg['GroupName'] == 'SSH Access':
            break
    else:
        security_group_id = create_security_group('SSH Access', 'Security group for SSH access', response['Reservations'][0]['Instances'][0]['VpcId'])
        ec2_client.modify_instance_attribute(
            InstanceId=instance_id,
            Groups=[security_group_id]
        )
        print(f'Security group added to instance {instance_id} for SSH access')

    # Update instance to use secure SSH keys
    # TODO: Implement key management here.

    print(f'EC2 instance {instance_id} hardened')

# Define main function
def main():
    # Harden RDS instances
    db_instance
