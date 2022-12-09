output "ssm_db_pass_name" {
  value = aws_ssm_parameter.db_pass.name
}


output "aws_ssm_parameter" {
  value = aws_ssm_parameter.key.value
}
output "aws_ssm_parameter" {
  value = aws_ssm_parameter.token.value
}