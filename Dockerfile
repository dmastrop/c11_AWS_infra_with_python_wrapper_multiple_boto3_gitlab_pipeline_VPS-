FROM python:3.11.9
WORKDIR /aws_EC2
COPY ./aws_EC2_boto3_class /aws_EC2
COPY ./EC2_key.pem /aws_EC2/sequential_master/EC2_key.pem
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "master_sequential_for_docker_run_in_linux_order_with_variable_delays_USE.py"]
