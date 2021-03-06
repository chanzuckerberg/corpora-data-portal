# Migrations task definition.
# 
data aws_region current {}

resource aws_ecs_task_definition task_definition {
  family        = "${var.custom_stack_name}-migration"
  network_mode  = "awsvpc"
  task_role_arn = var.task_role_arn
  container_definitions = <<EOF
[
  {
    "name": "db",
    "essential": true,
    "image": "${var.image}",
    "memory": 512,
    "environment": [
      {
        "name": "AWS_REGION",
        "value": "${data.aws_region.current.name}"
      },
      {
        "name": "AWS_DEFAULT_REGION",
        "value": "${data.aws_region.current.name}"
      },
      {
        "name": "REMOTE_DEV_PREFIX",
        "value": "/${var.custom_stack_name}"
      },
      {
        "name": "DATA_LOAD_PATH",
        "value": "${var.data_load_path}"
      },
      {
        "name": "DEPLOYMENT_STAGE",
        "value": "${var.deployment_stage}"
      }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "${aws_cloudwatch_log_group.cloud_watch_logs_group.id}",
        "awslogs-region": "${data.aws_region.current.name}"
      }
    },
    "command": ${jsonencode(split(",", var.cmd))}
  }
]
EOF
}

resource aws_cloudwatch_log_group cloud_watch_logs_group {
  retention_in_days = 365
  name              = "${var.custom_stack_name}/migrations"
}
