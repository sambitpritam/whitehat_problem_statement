#  Terraform Usage Documentation

## Executing Terraform Scripts

This section will guide you to execute the Terraform scripts to deploy an RDS DB MySql (free tier).

### Pre-requisites

Before executing the terraform scripts, there are few pre-requisties, mentioned below.

- Terraform `v1.0` installed. The scripts under `/terraform/` path is build using terraform version 1.0.
- AWS Configuration and Credentials should be available in the `~/.aws/config` and `~/.aws/credentials` files respectiviely for the desired user.

Contents for `~/.aws/credentials` is as follows:

```properties
[default]
aws_access_key_id=xxxx
aws_secret_access_key=xxxx
```

Content for `~/.aws/config`

```properties
[default]
region=xxxx
output=json
```


### Executing Terraform Scripts

Execute below commands to deploy RDS Instance to AWS Cluster.

```shell
$ cd ./terraform_scripts/
$ terraform init
$ terraform plan
$ terraform apply
```

To destroy the created resources, execute the below command

```shell
$ cd ./terraform_scripts/
$ terraform destroy
```



