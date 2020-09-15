# USAGE
This code is meant to get EC2 info from the default AWS account and region that is set in ```~/.aws/credentials```.

Moreover, this code creates a basic statistics report of your EC2 running instances and usage and sends it to ```sdtout``` as a JSON.

The ```Filters``` is set to pull information from all running EC2 instances, but you can change it in the following line:

```instances = ec2.describe_instances(Filters=[{'Name' : 'instance-state-name','Values' : ['running']}])```


# LIMITATIONS
* This code expects you to have an AWS account and credentials set-up as to [documentations shows](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html).
* As said, this code doesn't handle several accounts or several regions.
* Some of the fields are static (name,threadName,message and levelname).
