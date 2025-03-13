import boto3

def get_running_instance_ids(exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = []

    # Create an EC2 client
    ec2_client = boto3.client('ec2')

    try:
        # Describe instances with filters to get only running instances
        response = ec2_client.describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': ['running']
                }
            ]
        )
        
        # Extract instance IDs
        instance_ids = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                if instance_id not in exclude_ids:
                    instance_ids.append(instance_id)
        
        return instance_ids
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def stop_ec2_instances(instance_ids):
    # Create an EC2 client
    ec2_client = boto3.client('ec2')

    try:
        # Stop the instances
        response = ec2_client.stop_instances(InstanceIds=instance_ids)
        print("Stopping instances:", instance_ids)
        print(response)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace with your instance IDs to exclude
    exclude_ids = ['i-07139100f9fe32799', 'i-0ddbf7fda9773252b', 'i-0732df334cf72a173', 'i-0dcf3c32c9eb27580', 'i-06cfd334e2185f50a', 'i-02f502ffed943323b', 'i-09505844789cb6cc1', 'i-0c4cbe350c527ed22', 'i-08f19bbd0851ebcef', 'i-0837fb5a39ae707bf', 'i-007c8b4456e3c47c5', 'i-02b5d0832038f38f1', 'i-06b36bf3f3978a08f', 'i-0cb768b664e018ba6', 'i-09b7c12f4b164a1cb', 'i-0a9449b813fbe0ebe', 'i-07132a3adb01dde68']
    
    # Get running instance IDs excluding the specified IDs
    running_instance_ids = get_running_instance_ids(exclude_ids)
    print("Running Instance IDs (excluding specified IDs):", running_instance_ids)
    
    # Stop the running instances that are not in the exclusion list
    if running_instance_ids:
        stop_ec2_instances(running_instance_ids)
    else:
        print("No instances to stop.")

