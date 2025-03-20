import boto3
from dotenv import load_dotenv
import os
import paramiko

# Load environment variables from the .env file
load_dotenv()

# Set variables
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = os.getenv("region_name")
image_id = os.getenv("image_id")
instance_type = os.getenv("instance_type")
key_name = os.getenv("key_name")
min_count = os.getenv("min_count")
max_count = os.getenv("max_count")
aws_pem_key = os.getenv("AWS_PEM_KEY")

# Define the instance ID to exclude (the EC2 controller)
exclude_instance_id = 'i-0ddbf7fda9773252b'

# Establish a session with AWS
session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region_name
)

# Create an EC2 client
my_ec2 = session.client('ec2')

# Describe the running instances
response = my_ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

# Get the public IP addresses and security group IDs of the running instances except the excluded instance ID
public_ips = []
security_group_ids = []
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        if instance['InstanceId'] != exclude_instance_id:
            public_ips.append(instance['PublicIpAddress'])
            for sg in instance['SecurityGroups']:
                security_group_ids.append(sg['GroupId'])

# Define SSH details
port = 22
username = 'ubuntu'
key_path = 'EC2_generic_key.pem'

# Commands to install Tomcat server
commands = [
    'sudo DEBIAN_FRONTEND=noninteractive apt update -y',
    'sudo DEBIAN_FRONTEND=noninteractive apt install -y tomcat9',
    'sudo systemctl start tomcat9',
    'sudo systemctl enable tomcat9'
]

# Add a security group rule to allow access to port 80
for sg_id in set(security_group_ids):
    my_ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]
    )

# SSH into each instance and install Tomcat server
for ip in public_ips:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, key_filename=key_path)
    
    for command in commands:
        stdin, stdout, stderr = ssh.exec_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())
    
    ssh.close()

