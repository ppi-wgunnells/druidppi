"""
Script to provision services
Create roles and policies
"""

from cloudformation import CloudFormation
from deploy.vars import *

# profile='prod'
cloud = CloudFormation()


def open_template(a_name):
    with open(a_name, 'r') as data:
        template = data.read()
    return template


# blah = load.__open_template('deploy/dms/druid-dms-policy.yml')
# print(blah)

# ### Policies first
cloud.update_policies(glue_policies, 'glue')  # glue
cloud.update_policies(s3_policies, 's3')
cloud.update_policies(['druid-admin-sts-policy'], 'sts')  # sts
cloud.update_policies(['druid-dms-policy'], 'dms')  # dms entry
# cloud.validate_template(template_name='deploy/dms/druid-dms-policy.yml',
#                         load_template=open_template('deploy/dms/druid-dms-policy.yml'))


# ### Roles last
# druid glue developer
cloud.deploy_stack(name="druid-admin-role", path="role", parameters={
   "DruidAdminGluePolicy": "druid-admin-glue-policy",
   "DruidGluePolicy": "druid-glue-policy",
   "DruidBaseSettings": "druid-base-settings",
   "DruidS3Policy": "druid-s3-policy",
   "DruidAdminSTSPolicy": "druid-admin-sts-policy"
})
# ### one time deploy
# cloud.deploy_stack(name="AWSGlueServiceRole-druid-studio", path="role")
