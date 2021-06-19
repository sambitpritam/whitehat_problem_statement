# Ansible Usage Documentation

This Document will guide on setting up of Ansible on rpm based linux environment. This script will copy a file called `foo` from local system to remote ec2 isntances.

## Pre-Requisites

To execute ansible scripts on aws instances,

- Create ec2 instances with names `sample-instance-*`. This value can be changed in the hosts of `copy_file.yaml`.
- create private key `ec2.pem` files to connect to ec2 instances using ssh.
- Ensure the security group of EC2 Instances have ssh enabled
- Create aws configuration and credentials for python scripts execution: `~/.aws/credentials` and `~/.aws/config` with default profiles
- file `/home/ansible/foo` should be available in the mentioned location.

Content of `~/.aws/credentials`

```properties
[default]
aws_access_key_id=xxxx
aws_secret_access_key=xxxx
```

Content of `~/.aws/config`

```properties
[default]
region=us-west-2
output=json
```


## Environment Setup

### User Creation

- We need to create `ansible` user, that will have no password access to the machine.

    ```shell
    $ sudo useradd ansible
    $ echo "ansible ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/ansible
    $ sudo su ansible
    ```

### Installing Ansible

- We will install ansible from python3 package manager

    ```shell
    $ sudo su ansible
    $ sudo yum install -y python3
    $ sudo alternatives --set python /usr/bin/python3
    $ sudo yum install -y python3-pip
    $ pip3 install ansible --user
    $ pip3 install boto3 --user
    ```

- After installing, `ansible` using `pip3`, we need to add it to path. Installation using `--user` will install the application at `~/.local/bin`. Export this path tp environment varaible.

    ```shell
    $ vi ~/.bashrc
        export PATH=$PATH:"~/.local/bin/"
    $ source ~/.bashrc
    ```

- Validate Ansible installation

    ```shell
    $ ansible --version
    ```


### Dynamic Inventory Creation

- Dynamic Inventory is a way to extract the IP Address from the VPC using the API Services provided by the cloud provider.
- In case of AWS we will be using AWS SDK package `boto3` to eatract the host machine details.

    ```python
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

    ```

## Execution Commands:

```shell
$ cd ./ansible-scripts
$ chmod +x get_aws_running_hosts.py
$ ansible-playbook -i get_aws_running_hosts.py copy_file.yaml -u <EC2_USERNAME> --private-key=<PRIVATE_KEY_FILE>
```


