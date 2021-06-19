#! /bin/python3

import boto3
import json


def get_host_groups(ec2):
    all_groups = dict()

    for each_in in ec2.instances.filter(Filters=[{"Name": "instance-state-name", "Values": ["running"]}]):
        for tag in each_in.tags:
            if tag["Key"] in all_groups:
                hosts = all_groups.get(tag["Key"])
                hosts.append(each_in.public_ip_address)
                all_groups[tag["Key"]] = hosts
            else:
                hosts = [each_in.public_ip_address]
                all_groups[tag["Key"]] = hosts

            if tag["Value"] in all_groups:
                hosts = all_groups.get(tag["Value"])
                hosts.append(each_in.public_ip_address)
                all_groups[tag["Value"]] = hosts
            else:
                hosts = [each_in.public_ip_address]
                all_groups[tag["Value"]] = hosts
            
    return all_groups

if __name__ == "__main__":
    ec2 = boto3.resource("ec2")
    all_groups = get_host_groups(ec2)
    inventory = dict()

    for key, value in all_groups.items():
        hosts_obj = {"hosts": value}
        inventory[key] = hosts_obj
    
    print(json.dumps(inventory))