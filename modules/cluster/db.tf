resource "aws_db_instance" "db_instance" {
  allocated_storage    = 10
  engine               = var.engine
  engine_version       =  var.engine_version
  instance_class       =  var.instance_class
  ca_cert_identifier   = "rds-ca-2019"
  vpc_security_group_ids  = [aws_security_group.db_security_group.id]
  db_subnet_group_name      = aws_db_subnet_group.default.name
  identifier           = var.db_name
  username             = var.username //postgres
  name                 = "weather"
  password             = data.aws_ssm_parameter.password_db.value
  parameter_group_name = "default.postgres12"
  skip_final_snapshot  = true
}


resource "aws_db_subnet_group" "default" {
  name = "${var.app_name}-${var.environment}-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id
}
