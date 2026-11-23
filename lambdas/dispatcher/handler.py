import json
import os
import boto3
from typing import Dict, Any, List

dynamodb = boto3.resource("dynamodb")
stepfunctions = boto3.client("stepfunctions")

LOCK_TABLE_NAME = os.getenv("LOCK_TABLE_NAME", "incident-aggregation-locks")
AGGREGATION_WINDOW_SECONDS = 60

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Ingress Dispatcher implementing ADR-02:
    Buffers incoming CloudWatch alarms from SQS FIFO, aggregates burst alerts
    within a 60-second window using a DynamoDB correlation lock, and prevents
    alert storms from spawning redundant multi-agent investigations.
    """
    records: List[Dict[str, Any]] = event.get("Records", [])
    if not records:
        return {"status": "no_records"}
    
    table = dynamodb.Table(LOCK_TABLE_NAME)
    aggregated_alerts = []
    
    for record in records:
        body = json.loads(record.get("body", "{}"))
        service_name = body.get("detail", {}).get("service", "unknown-service")
        alarm_name = body.get("detail", {}).get("alarmName", "generic-alarm")
        
        lock_key = f"incident-lock:{service_name}"
        now_ts = int(record.get("attributes", {}).get("ApproximateReceiveTimestamp", "0")) // 1000
        
        # Try acquiring aggregation lock (conditional write)
        try:
            table.put_item(
                Item={
                    "lock_id": lock_key,
                    "service_name": service_name,
                    "first_alarm": alarm_name,
                    "expires_at": now_ts + AGGREGATION_WINDOW_SECONDS
                },
                ConditionExpression="attribute_not_exists(lock_id) OR expires_at < :now",
                ExpressionAttributeValues={":now": now_ts}
            )
            # Lock acquired: This alarm initializes the incident investigation
            aggregated_alerts.append(body)
            print(f"[LOCK ACQUIRED] Initializing RCA for service: {service_name}")
            
        except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
            # Active aggregation window exists: Alert storm buffered and de-duplicated
            print(f"[BUFFERED & DE-DUPLICATED] Alarm {alarm_name} aggregated for {service_name}")
            continue

    return {
        "status": "processed",
        "initialized_incidents_count": len(aggregated_alerts)
    }
