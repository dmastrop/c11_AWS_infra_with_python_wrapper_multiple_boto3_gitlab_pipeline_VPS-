import boto3

def create_ec2_instances(num_instances):
    # Create a session using your AWS credentials
    session = boto3.Session(
        aws_access_key_id='***REMOVED***',
        aws_secret_access_key='***REMOVED***',
        region_name='us-east-1'
    )

    # Create an EC2 resource
    ec2 = session.resource('ec2')

    # Create the specified number of EC2 instances
    instances = ec2.create_instances(
        ImageId='ami-0e1bed4f06a3b463d',  # Replace with your desired AMI ID
        MinCount=num_instances,
        MaxCount=num_instances,
        InstanceType='t2.micro',  # Replace with your desired instance type
        KeyName='course3_kops_from_course8_project14_EC2_key'  # Replace with your key pair name
    )

    for instance in instances:
        print(f'Created instance with ID: {instance.id}')

if __name__ == "__main__":
    create_ec2_instances(10)

