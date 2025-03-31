import boto3
import json
import os
from dotenv import load_dotenv
import logging
import time

# Initialize logger
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

# Load environment variables from the .env file
load_dotenv()

# Set variables from environment
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = os.getenv("region_name")

# Check for missing environment variables
if not aws_access_key or not aws_secret_key or not region_name:
    logger.error("Missing AWS credentials or region name in environment variables.")
    raise ValueError("Missing AWS credentials or region name in environment variables.")

# Establish a session with AWS
session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region_name
)

# Create clients
elb_client = session.client('elbv2')
acm_client = session.client('acm')
route53_client = session.client('route53')
autoscaling_client = session.client('autoscaling')



# Load instance and security group IDs from JSON file
with open('instance_ids.json', 'r') as f:
    data = json.load(f)
    instance_ids = data['instance_ids']
    security_group_ids = data['security_group_ids']

# Retrieve the load balancer ARN and DNS name
load_balancers = elb_client.describe_load_balancers()
load_balancer_arn = load_balancers['LoadBalancers'][0]['LoadBalancerArn']
load_balancer_dns_name = load_balancers['LoadBalancers'][0]['DNSName']

print(f"Load Balancer DNS Name: {load_balancer_dns_name}")



# Create Auto Scaling Group
autoscaling_client.create_auto_scaling_group(
    AutoScalingGroupName='my-auto-scaling-group',
    InstanceId=instance_ids[0],  # Use the first instance ID from your list
    MinSize=1,
    MaxSize=10,
    DesiredCapacity=2,
    VPCZoneIdentifier=','.join(security_group_ids),
    TargetGroupARNs=[tomcat_target_group_arn],
    Tags=[
        {
            'Key': 'Name',
            'Value': 'my-auto-scaling-group'
        }
    ]
)

print("Auto Scaling Group created")

# Create scaling policies
autoscaling_client.put_scaling_policy(
    AutoScalingGroupName='my-auto-scaling-group',
    PolicyName='scale-out-policy',
    PolicyType='TargetTrackingScaling',
    TargetTrackingConfiguration={
        'PredefinedMetricSpecification': {
            'PredefinedMetricType': 'ASGAverageCPUUtilization'
        },
        'TargetValue': 50.0
    }
)

autoscaling_client.put_scaling_policy(
    AutoScalingGroupName='my-auto-scaling-group',
    PolicyName='scale-in-policy',
    PolicyType='TargetTrackingScaling',
    TargetTrackingConfiguration={
        'PredefinedMetricSpecification': {
            'PredefinedMetricType': 'ASGAverageCPUUtilization'
        },
        'TargetValue': 20.0
    }
)

print("Scaling policies created")

