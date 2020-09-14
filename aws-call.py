import boto3
import json
import datetime
import logging
import pythonjsonlogger
from pythonjsonlogger import jsonlogger

#starting a pipeline between aws to the 
ec2 = boto3.client('ec2')

#added the function the fix JSON problem with the datetime exportation of AWS
def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

# create a list of instances according to the filters chosen.
# this example filters all the ec2 instances that are running.
instances = ec2.describe_instances(Filters=[{'Name' : 'instance-state-name','Values' : ['running']}])

#testing JSON output
#print(json.dumps(instances['Reservations'][0]['Instances'][0]['LaunchTime'], indent=4, sort_keys=True, default=datetime_handler))

#getting only the list of instances info
#me = instances['Reservations']
publicip_list = []
names_list = []
running_time_list = []
num_of_instances = len(instances)
count=0
time = str(datetime.datetime.today())
threadName = 'MainThread'
message = 'testing K8S REPORTING'
levelname = 'INFO'
name = 'K8S REPORTS'

while count < num_of_instances:
    instance = instances['Reservations'][count]['Instances'][0]
    publicip_list.append(instance['PublicIpAddress'])
    running_time_list.append(str(datetime.datetime.now().replace(tzinfo=None)-instances['Reservations'][0]['Instances'][0]['LaunchTime'].replace(tzinfo=None)))
    for j in instance["Tags"]:
        if j["Key"] == "Name":
            #get only the tag "Name"
            names_list.append(j["Value"])
    count=count+1


report={
    'threadName':'MainThread',
    "name": "K8S REPORTS",
    "time": datetime.datetime.today(),
    "running instances": num_of_instances,
    "instance IPs": publicip_list,
    'instance name': names_list,
    'running time': running_time_list,
    'message': "testing K8S REPORTING",
    "levelname": "INFO",
}

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        return super().add_fields(log_record, record, message_dict)
        
# starting the JSON to the handler
handler = logging.StreamHandler()
# setting the format for the report
#format_str = '%(threadName)%(name)%(time)%(num_of_instances)'
format_str = '%(message)%(levelname)%(name)%(asctime)'
formatter = pythonjsonlogger.jsonlogger.JsonFormatter(format_str)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
# Normally we would attach the handler to the root logger, and this would be unnecessary
logger.debug(formatter)
logger.propagate = False