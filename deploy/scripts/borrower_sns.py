"""
Simple script to send alerts to SNS topic
"""
import boto3
import json

session = boto3.Session()


def sns_topic_arn(stage):
    return f"arn:aws:sns:us-west-2:492436075634:borrower_check_{stage}"


def arn(stage):
    return f'arn:aws:lambda:us-west-2:492436075634:function:borrower_check-{stage}'


def fanout_configs(stage):
    sns_topic_policy = {
            "Sid": "STSPolicy",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "sns:Publish",
            "Resource": sns_topic_arn(stage),
            "Condition": {
                "ArnEquals": {"AWS:SourceArn": f"arn:aws:sts::492436075634:assumed-role/borrower_check-dev/borrower_check-{stage}"},
                },
        }
    sns_lamb_policy = {
            "Sid": "BorrowerLambPolicy",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "sns:Publish",
            "Resource": sns_topic_arn(stage),
            "Condition": {
                "ArnLike": {"AWS:SourceArn": f"{arn(stage)}"},
                },
        }

    sns_policy = {
        "Version": "2012-10-17",
        "Statement": [sns_topic_policy, sns_lamb_policy],
    }

    return sns_policy


def message(subject, sns_msg, topic):
    """
    :param subject: str() of subject
    :param sns_msg: str() of sns message to send
    :param topic: str() of topic name
    :return: dict() of message
    """
    response = boto3.client('sns', region_name='us-west-2').publish(
        Subject=subject,
        Message=sns_msg,
        TopicArn=f"arn:aws:sns:us-west-2:492436075634:{topic}"
    )
    return response


def set_topic_attribute(arn, att_type, att_val):
    """
    Special attr names: LambdaFailureFeedbackRoleArn, LambdaSuccessFeedbackRoleArn, LambdaSuccessFeedbackSampleRate
    :param arn: str() of topic ARN
    :param att_type: str() of attribute Name 'Policy' or 'PolicyFilter' or Special
    :param att_val: str() or json.dumps(sns_policy)
    :return: dict()
    """
    client = session.client('sns', region_name='us-west-2')
    try:
        response = client.set_topic_attributes(
            TopicArn=arn,
            AttributeName=att_type,
            AttributeValue=att_val
        )
        return response
    except Exception as err:
        return err


if __name__ == "__main__":
    env = 'prod'
    # topic_name = f'borrower_check_{env}'
    # print(message(subject=f"borrower check {env}", sns_msg="This manual job failed", topic=topic_name))
    sns_res = set_topic_attribute(sns_topic_arn(env), 'Policy', json.dumps(fanout_configs(env)))
    print(sns_res)
