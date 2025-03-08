import boto3

def terminate_ec2_instances(instance_ids, aws_access_key, aws_secret_key, region_name):
    # Establish a session with AWS
    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region_name
    )
    
    my_ec2_client = session.client('ec2')
    
    response = my_ec2_client.terminate_instances(InstanceIds=instance_ids)
    
    return response

# Example usage
instance_ids = ['i-0fe5ff6f4a697a6bc', 'i-0571e860630e6b1da', 'i-01de18e9e9b7ac070', 'i-0eddc4c4e48703107', 'i-0b55a689abef24bfc', 'i-0190749537784ee84', 'i-0e3a1b78df870dcb0', 'i-01ef77bde6035e886', 'i-071e6714e341a03ab', 'i-0a1225837f4dead95']
aws_access_key = '***REMOVED***'
aws_secret_key = '***REMOVED***'
region_name = 'us-east-1'


response = terminate_ec2_instances(instance_ids, aws_access_key, aws_secret_key, region_name)
print(response)
