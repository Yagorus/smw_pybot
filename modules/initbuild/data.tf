data "aws_caller_identity" "current" { }

data "aws_ssm_parameter" "bot_token" {
    depends_on = [
      aws_ssm_parameter.token
    ]
  name = aws_ssm_parameter.token.name
}
data "aws_ssm_parameter" "bot_key" {
    depends_on = [
      aws_ssm_parameter.key
    ]
  name = aws_ssm_parameter.key.name
}

