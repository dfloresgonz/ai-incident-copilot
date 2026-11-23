terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.50"
    }
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = "ai-incident-copilot"
      Environment = "production"
      ManagedBy   = "Terraform"
    }
  }
}

# SQS FIFO Ingress Buffer (ADR-02)
resource "aws_sqs_queue" "incident_alerts_fifo" {
  name                        = "incident-alerts.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
  message_retention_seconds   = 86400
  visibility_timeout_seconds  = 120
}

# DynamoDB Alert Aggregation Lock Table (ADR-02)
resource "aws_dynamodb_table" "aggregation_lock" {
  name         = "incident-aggregation-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "lock_id"

  attribute {
    name = "lock_id"
    type = "S"
  }

  ttl {
    attribute_name = "expires_at"
    enabled        = true
  }
}

# EventBridge Rule routing CloudWatch alarms to SQS FIFO
resource "aws_cloudwatch_event_rule" "p1_alarms" {
  name        = "capture-p1-incident-alarms"
  description = "Routes critical 5xx and latency alarms to SQS FIFO buffer"

  event_pattern = jsonencode({
    "source"      : ["aws.cloudwatch"],
    "detail-type" : ["CloudWatch Alarm State Change"],
    "detail" : {
      "state" : {
        "value" : ["ALARM"]
      }
    }
  })
}

resource "aws_cloudwatch_event_target" "sqs_target" {
  rule      = aws_cloudwatch_event_rule.p1_alarms.name
  target_id = "SendToSQSFIFO"
  arn       = aws_sqs_queue.incident_alerts_fifo.arn

  sqs_target {
    message_group_id = "ProductionAlarms"
  }
}
