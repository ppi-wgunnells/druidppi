"""
Create sns for multiple environments
"""
import boto3

session = boto3.Session()


def create_topic(name, tags):
    client = session.client('sns', region_name='us-west-2')
    return client.create_topic(Name=name, Tags=tags)


if __name__ == "__main__":
    env = 'prod'
    bc_name = f"borrower_check_{env}"
    tag = {'Key': 'dev', 'Value': bc_name}
    create_topic(name=bc_name, tags=[tag])
