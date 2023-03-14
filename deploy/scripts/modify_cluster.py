"""
modify cluster rds cluster to add IAM
"""
import boto3


session = boto3.session.Session()

sts_session = boto3.Session()
sts_client = sts_session.client('sts')
cred = sts_client.assume_role(
    RoleArn="arn:aws:iam::492436075634:role/druid-admin-role-Role-SET2TUJYEJZT",
    RoleSessionName="druid-dev-session2"
)
access_key = cred['Credentials']['AccessKeyId']
secret_key = cred['Credentials']['SecretAccessKey']
session_key = cred['Credentials']['SessionToken']


db_session = boto3.Session(aws_secret_access_key=secret_key,
                           aws_access_key_id=access_key,
                           aws_session_token=session_key)


def modify_cluster(identifier):
    client = db_session.client('rds')
    response = client.modify_db_cluster(
        DBClusterIdentifier=identifier,
        ApplyImmediately=True,
        EnableIAMDatabaseAuthentication=True
    )
    return response


if __name__ == "__main__":
    # ### print(modify_cluster('consortium-aurora-dev'))  # complete
    # ### print(modify_cluster('cms-prod-cluster-cluster'))  # complete
    # ### print(modify_cluster('consortium-aurora-prod'))  # complete
    pass
