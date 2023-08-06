import json
import subprocess

ami_id = "ami-08dc6d0e9a4b6af61" # Image ID
instance_type = 'p3.2xlarge' # Instance Type
key_name = 'Assaf' # key-pair name
security_groups = "launch-wizard-10" # security group
max_price = '1.5'  # maximum price
instance_name_tag = 'Name of instance'

startup_script = "#!/bin/bash\\n" \
            "echo 'This is an example' \\n"



#### DO NOT CHANGE ###
market_type_dict = {"MarketType": "spot", "SpotOptions": {"MaxPrice": max_price, "SpotInstanceType": "persistent",
                                                          "InstanceInterruptionBehavior": "stop"}}
market_type_json = json.dumps(market_type_dict)
tag_dict = [{"ResourceType": "instance", "Tags": [{"Key": "Name", "Value": instance_name_tag}]},
            ]
tag_json = json.dumps(tag_dict)
launch_command = ["aws", "ec2", "run-instances", "--image-id", "{ami_id}".format(ami_id=ami_id),
                  "--instance-type", "{instance_type}".format(instance_type=instance_type), "--key-name",
                  "{key_name}".format(key_name=key_name), "--security-groups",
                  "{secutiry_groups}".format(secutiry_groups=security_groups), "--user-data",
                  "{user_data}".format(user_data=startup_script),
                  "--instance-market-options", "{market_type}".format(market_type=market_type_json),
                  "--tag-specifications",
                  "{tag_string}".format(tag_string=tag_json)]

result = subprocess.run(launch_command, stdout=subprocess.PIPE)
result_dict = json.loads(result.stdout.decode('utf-8'))
tag_spot_command = ["aws", "ec2", "create-tags", "--resources",
                    result_dict['Instances'][0]['SpotInstanceRequestId'],
                    "--tags", 'Key="Name",Value="{}"'.format(instance_name_tag)]
#### DO NOT CHANGE ###