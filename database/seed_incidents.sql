-- Sample historical incidents for development & testing
INSERT INTO incidents (incident_number, service_name, error_signature, root_cause, remediation_steps, ssm_runbook, postmortem_summary)
VALUES 
(
    'INC-2025-089',
    'checkout-service',
    'HTTP 504 Gateway Timeout DeadlockDetected',
    'Connection pool exhaustion in checkout service due to unindexed foreign key queries during flash sale.',
    'Execute SSM runbook restart_ecs_service to clear orphaned connections, followed by scaling database connection limit.',
    'AWS-RestartECSService',
    'High concurrency caused PostgreSQL connection pool starvation. Latency spiked to 12s on /checkout/pay.'
),
(
    'INC-2025-112',
    'payment-gateway',
    'HTTP 500 OutOfMemoryError Java heap space',
    'Memory leak in payment token serialization introduced in commit 8f4c21a.',
    'Trigger automated deployment rollback to commit b1e4902 using SSM rollback runbook.',
    'AWS-RollbackDeployment',
    'Heap memory climbed monotonically over 3 hours following production deployment v2.14.0.'
),
(
    'INC-2025-144',
    'order-service',
    'HTTP 503 Service Unavailable ConnectionRefused',
    'Fargate task crash loop caused by invalid configuration parameter in AWS AppConfig.',
    'Rollback AppConfig deployment to previous configuration version and restart task fleet.',
    'AWS-RestartECSService',
    'Microservice failed health checks immediately on startup due to syntax error in JSON config.'
)
ON CONFLICT (incident_number) DO NOTHING;
