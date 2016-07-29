import boto3
import base64
import uuid
import datetime


class Cluster:
    def __init__(self,access_key_id='',secret_key_id='', ami='ami-18a16e78',key='',instance_type='t1.micro',region='us-west-2'):
        self.dryrun = False
        self.fleet_id = ''
        self.az = ''
        self.region = region
        self.access_key = access_key_id
        self.secret_key = secret_key_id
        self.client = boto3.client('ec2',
                                   region_name=self.region,
                                   aws_access_key_id=self.access_key,
                                   aws_secret_access_key=self.secret_key)
        #self.instance_count = 1
        self.user_data = ''
        self.data = ''
        self.ami = ami
        self.instance_type = instance_type
        self.key = key
        self.config = config = {
            #'UserData':self.data,
            'ImageId':self.ami,
            'InstanceType':self.instance_type,
            'KeyName':self.key
        }
    def _get_fleet_role_arn(self):
        iam = boto3.resource('iam',
                             region_name=self.region,
                             aws_access_key_id=self.access_key,
                             aws_secret_access_key=self.secret_key)
        role = iam.Role('aws-ec2-spot-fleet-role')
        return role.arn

    def get_user_data(self):
        pass

    def _get_spot_price_estimate(self):
        data = self.client.describe_spot_price_history(DryRun=False,
                                                       StartTime=datetime.datetime.now(),
                                                       EndTime=datetime.datetime.now(),
                                                       InstanceTypes=[self.instance_type],
                                                       ProductDescriptions=['Linux/UNIX'])
        av_zones = {estimate['AvailabilityZone']:float(estimate['SpotPrice']) for estimate in data['SpotPriceHistory']}
        self.az = max(av_zones,key=lambda x: av_zones[x])
        max_price = av_zones[self.az]
        return max_price+0.001

    def request_spot_instance(self,n=1):
        estimated_price = str(self._get_spot_price_estimate())
        instance_count = n
        return self.client.request_spot_instances(
            DryRun=False,
            SpotPrice=estimated_price,
            ClientToken=str(uuid.uuid1()),
            InstanceCount=instance_count,
            Type='one-time',
            LaunchSpecification=self.config
        )

    def request_spot_fleet(self,n=1):
        estimated_price = str(self._get_spot_price_estimate())
        instance_count = n
        spotfleetrequestconfig = {
            'ClientToken': str(uuid.uuid1()),
            'SpotPrice': estimated_price,
            'TargetCapacity': n,
            'LaunchSpecifications':[self.config],
            'TerminateInstancesWithExpiration': False,
            'IamFleetRole': self._get_fleet_role_arn()
        }
        request = self.client.request_spot_fleet(DryRun=self.dryrun,
                                              SpotFleetRequestConfig=spotfleetrequestconfig)
        return request['SpotFleetRequestId']

    def cancel_fleet_request(self,fleet_ids,termination=True):

        return self.client.cancel_spot_fleet_requests(
            DryRun=False,
            SpotFleetRequestIds=[fleet_ids],
            TerminateInstances=termination
        )

    def check_instance(self):
        pass
    def launch(self,n=1):
        self.fleet_id = self.request_spot_fleet(n)

