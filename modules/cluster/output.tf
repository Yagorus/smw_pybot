output "subnets" {
  value = aws_subnet.private[*].id
}

output "vpc_id" {
  value = aws_vpc.main.id
}

output "address" {
  value = aws_db_instance.db_instance.address
}
output "arn" {
  value = aws_db_instance.db_instance.arn
}
output "id" {
  value = aws_db_instance.db_instance.id
}
output "prot" {
  value = aws_db_instance.db_instance.port
}
output "username" {
  value = aws_db_instance.db_instance.username
}
output "endpoint" {
  value = aws_db_instance.db_instance.endpoint
}
