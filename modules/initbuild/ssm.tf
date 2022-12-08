resource "aws_ssm_parameter" "token" {
  name  = "BOT_TOKEN"
  type  = "String"
  value = var.bot_token
  overwrite = false
  tags = {
    Name = "${var.app_name}-${var.environment}-token"
  }
}

resource "aws_ssm_parameter" "key" {
  name  = "API_KEY"
  type  = "String"
  value = var.bot_key
  overwrite = false
  tags = {
    Name = "${var.app_name}-${var.environment}-key"
  }
}

resource "aws_ssm_parameter" "db_pass" {
  name  = "DB_PASS"
  type  = "String"
  value = var.db_password
  overwrite = false
  tags = {
    Name = "${var.app_name}-${var.environment}-key"
  }
}