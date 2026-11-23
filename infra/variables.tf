variable "aws_region" {
  type        = string
  description = "AWS Deployment Region"
  default     = "us-east-1"
}

variable "environment" {
  type        = string
  description = "Target deployment environment"
  default     = "production"
}
