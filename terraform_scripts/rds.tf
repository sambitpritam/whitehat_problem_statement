resource "aws_db_instance" "mysql-rds" {
    identifier = "mysqlrds"
    storage_type = "gp2"
    availability_zone = var.aws_az

    # mysql db details
    allocated_storage = 20
    engine = "mysql"
    engine_version = var.mysql_engine_version
    instance_class = "db.t2.micro"
    port = "3306"

    name = "mysqlrdsdb"
    username = var.mysql_username
    password = var.mysql_password
    parameter_group_name = "default.mysql8.0"
    

    publicly_accessible = true
    deletion_protection = false
    skip_final_snapshot = true

    tags = {
        Name = "MySQL RDS Instance"
    }
}