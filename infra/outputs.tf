output "sqs_queue_arn" {
  description = "ARN of the SQS FIFO Alert Buffer"
  value       = aws_sqs_queue.incident_alerts_fifo.arn
}

output "dynamodb_lock_table_name" {
  description = "Name of the DynamoDB Aggregation Lock Table"
  value       = aws_dynamodb_table.aggregation_lock.name
}
