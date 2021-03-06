variable vpc {
  type        = string
  description = "The VPC that the ECS cluster is deployed to"
}

variable custom_stack_name {
  type        = string
  description = "Please provide the stack name"
}

variable app_name {
  type        = string
  description = "Please provide the ECS service name"
}

variable cluster {
  type        = string
  description = "Please provide the ECS Cluster ID that this service should run on"
}

variable image {
  type        = string
  description = "Image name"
}

variable service_port {
  type        = number
  description = "What port does this service run on?"
  default     = 80
}

variable desired_count {
  type        = number
  description = "How many instances of this task should we run across our cluster?"
  default     = 2
}

variable listener {
  type        = string
  description = "The Application Load Balancer listener to register with"
}

variable host_match {
  type        = string
  description = "Host header to match for target rule"
}

variable security_groups {
  type        = string
  description = "Security groups for ECS tasks"
}

variable subnets {
  type        = string
  description = "Subnets for ecs tasks"
}

variable task_role_arn {
  type        = string
  description = "ARN for the role assumed by tasks"
}

variable path {
  type        = string
  description = "The path to register with the Application Load Balancer"
  default     = "/*"
}

variable cmd {
  type        = string
  description = "The path to register with the Application Load Balancer"
  default     = ""
}

variable api_url {
  type        = string
  description = "URL for the backend api."
}

variable frontend_url {
  type        = string
  description = "URL for the frontend app."
}

variable deployment_stage {
  type        = string
  description = "The name of the deployment stage of the Application"
  default     = "dev"
}

variable step_function_arn {
  type        = string
  description = "ARN for the step function called by the uploader"
}

variable priority {
  type        = number
  description = "Listener rule priority number within the given listener"
}
