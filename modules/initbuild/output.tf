output "ssm_db_pass_name" {
  value = aws_ssm_parameter.db_pass.name
}

output "db_password" {
  value = var.db_password
}
output "bot_token" {
  value = var.bot_token
}
output "bot_key" {
  value = var.bot_key
}