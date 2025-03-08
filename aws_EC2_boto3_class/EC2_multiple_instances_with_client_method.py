import boto3

def start_ec2_instances(aws_access_key, aws_secret_key, region_name, image_id, instance_type, key_name, min_count, max_count):
    # Establish a session with AWS
    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region_name
    )
    
    # Create an EC2 client
    my_ec2 = session.client('ec2')
    
    # Start EC2 instances
    response = my_ec2.run_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        KeyName=key_name,
        MinCount=min_count,
        MaxCount=max_count
    )
    
    return response

# Example usage
aws_access_key = '***REMOVED***'
aws_secret_key = '***REMOVED***'
region_name = 'us-east-1'
image_id = 'ami-0e1bed4f06a3b463d'  # Replace with your desired AMI ID
instance_type = 't2.micro'  # Replace with your desired instance type
key_name = 'course3_kops_from_course8_project14_EC2_key'  # Replace with your key pair name
min_count = 10  # Minimum number of instances to launch
max_count = 10  # Maximum number of instances to launch

response = start_ec2_instances(aws_access_key, aws_secret_key, region_name, image_id, instance_type, key_name, min_count, max_count)
print(response)

