from typing import Dict, Any
from agent.state import IncidentState

def telemetry_agent_node(state: IncidentState) -> Dict[str, Any]:
    """
    Observability Agent: Interacts with mcp-cloudwatch server to retrieve
    P99 latency, error rates, and top stack traces from CloudWatch Logs Insights.
    """
    service_name = state.get("service_name")
    
    # Mocking MCP tool call response for local execution harness
    metrics = {
        "p99_latency_ms": 11850,
        "http_5xx_rate_pct": 14.8,
        "db_connection_pool_usage_pct": 100.0,
        "cpu_utilization_pct": 42.1
    }
    
    error_logs = [
        "2026-11-23T03:02:11Z [ERROR] connection pool exhausted: timeout waiting for connection (pool size=50)",
        "2026-11-23T03:02:15Z [ERROR] HTTP 504 Gateway Timeout on /checkout/pay duration=12003ms",
        "2026-11-23T03:02:19Z [ERROR] DeadlockDetected: transaction aborted while locking record in orders_partition"
    ]
    
    return {
        "cloudwatch_metrics": metrics,
        "error_logs": error_logs
    }
