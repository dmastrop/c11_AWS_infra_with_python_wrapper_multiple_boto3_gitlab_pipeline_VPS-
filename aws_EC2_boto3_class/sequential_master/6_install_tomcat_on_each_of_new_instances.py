import boto3
import paramiko

# Define the instance ID to exclude (the EC2 controller)
exclude_instance_id = 'i-0ddbf7fda9773252b'


# Create an EC2 client with the specified region
#ec2 = boto3.client('ec2', region_name='us-west-2')


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

# Get the public IP addresses of the running instances except the excluded instance ID
public_ips = []
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        if instance['InstanceId'] != exclude_instance_id:
            public_ips.append(instance['PublicIpAddress'])

# Define SSH details
port = 22
username = 'ubuntu'
key_path = 'EC2_key.pem'

# Commands to install Tomcat server
commands = [
    'sudo yum update -y',
    'sudo yum install -y tomcat',
    'sudo systemctl start tomcat',
    'sudo systemctl enable tomcat'
]

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

