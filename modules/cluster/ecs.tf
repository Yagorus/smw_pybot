resource "aws_ecs_cluster" "aws_ecs_cluster" {
  depends_on = [
    aws_ecs_capacity_provider.capacity_provider,
    aws_autoscaling_group.autoscale
  ]
  name = "${var.app_name}-${var.environment}-cluster"
  capacity_providers = [aws_ecs_capacity_provider.capacity_provider.name]
  tags = {
    Name = "${var.app_name}-${var.environment}-cluster"
  }
}

resource "aws_ecs_task_definition" "aws_ecs_task" {
  family = "${var.app_name}-${var.environment}-task"
  network_mode             = "awsvpc"
  execution_role_arn       = aws_iam_role.ecsTaskExecutionRole.arn
  task_role_arn            = aws_iam_role.ecsTaskExecutionRole.arn
  #container_definitions    = data.template_file.cb_bot.rendered
  
  container_definitions     = jsonencode(
[
  {
    name = "${var.app_name}-${var.environment}-container"
    image = "${local.app_image}"
    memory = 512
    cpu = 256
    essential = true
    
    portMappings = [
      {
        "containerPort": var.app_port,
        "hostPort": var.app_port
      }
    ]

    logConfiguration =  {
       logDriver = "awslogs"
       options ={
           awslogs-group = "${var.app_name}-${var.environment}-ecs-log"
           awslogs-region = var.aws_region
           awslogs-stream-prefix ="ecs"
       }
   }

  environment = [
     {
       name ="APP_DATABASE_URL"
       value = "postgresql://${aws_db_instance.db_instance.username}:${data.aws_ssm_parameter.password_db.value}@${aws_db_instance.db_instance.address}/${aws_db_instance.db_instance.name}"
     }
  ]
}
])

}


resource "aws_ecs_service" "main" {
  depends_on = [aws_iam_role.ecsTaskExecutionRole]
  name            = "${var.app_name}-${var.environment}-service"
  cluster         = aws_ecs_cluster.aws_ecs_cluster.id
  task_definition = aws_ecs_task_definition.aws_ecs_task.arn
  desired_count   = 1
  deployment_minimum_healthy_percent = "90"


  network_configuration {
        security_groups = [aws_security_group.security_group_port_i80.id]
        subnets =aws_subnet.private.*.id     
        
    }

  capacity_provider_strategy {
    capacity_provider = aws_ecs_capacity_provider.capacity_provider.name
    weight = 1
    base = 0
  }
}

resource "aws_ecs_capacity_provider" "capacity_provider" {
  name = "${var.app_name}-${var.environment}-capacity-provider"

  auto_scaling_group_provider {
    auto_scaling_group_arn         = aws_autoscaling_group.autoscale.arn
    managed_termination_protection = "DISABLED"
  
    managed_scaling {
      maximum_scaling_step_size = 2
      minimum_scaling_step_size = 1
      status                    = "ENABLED"
      target_capacity           = 100
    }
  }
}

resource "aws_cloudwatch_log_group" "log_group" {
  name              = "${var.app_name}-${var.environment}-ecs-log"
  retention_in_days = 30

  tags = {
    Name = "cb-log-group"
  }
}