import boto3
import json
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO)  #allows seeing INFO level logs

#starting a pipeline between aws to the 
ec2 = boto3.client('ec2')

#added the function the fix JSON problem with the datetime exportation of AWS
def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

# create a list of instances according to the filters chosen.
# this example filters all the ec2 instances that are running.
instances = ec2.describe_instances(Filters=[{'Name' : 'instance-state-name','Values' : ['running']}])

#testing JSON output
#print(json.dumps(instances['Reservations'][0]['Instances'][0]['LaunchTime'], indent=4, sort_keys=True, default=datetime_handler))


publicip_list = []
names_list = []
running_time_list = []
num_of_instances = len(instances)
count=0


while count < num_of_instances:
    instance = instances['Reservations'][count]['Instances'][0]
    publicip_list.append(instance['PublicIpAddress'])
    running_time_list.append(str(datetime.now().replace(tzinfo=None)-instances['Reservations'][0]['Instances'][0]['LaunchTime'].replace(tzinfo=None)))
    for j in instance["Tags"]:
        if j["Key"] == "Name":
            #get only the tag "Name"
            names_list.append(j["Value"])
    count=count+1

#starting a logger
logger = logging.getLogger('K8S REPORTS')

report={
    'threadName':'MainThread',
    'name': 'K8S REPORTS',
    'time': datetime.now().strftime("%d/%m/%Y"),
    'running instances': num_of_instances,
    'instance IPs': publicip_list,
    'instance name': names_list,
    'running time': running_time_list,
    'message': 'testing K8S REPORTING',
    'levelname': 'INFO'
}

logger.info(report)