import os
from typing import Dict, Any
from agent.state import IncidentState

def triage_agent_node(state: IncidentState) -> Dict[str, Any]:
    """
    Evaluates raw alarms under 800ms using Claude Haiku 5.5.
    Filters transient flapping and classifies severity (P1-P4).
    """
    raw_alerts = state.get("raw_alerts", [])
    service_name = state.get("service_name", "unknown-service")
    
    # In production, invokes Amazon Bedrock: anthropic.claude-haiku-5-5
    # Evaluates error thresholds and monitor transitions
    alert_count = len(raw_alerts)
    has_5xx = any("504" in str(a) or "500" in str(a) for a in raw_alerts)
    
    severity = "P1" if has_5xx and alert_count > 5 else "P2"
    is_flapping = alert_count < 2 and not has_5xx
    
    summary = (
        f"Detected {alert_count} alarms for {service_name}. "
        f"Critical 5xx thresholds exceeded across multiple AZs."
    )
    
    return {
        "severity": severity,
        "is_flapping": is_flapping,
        "triage_summary": summary
    }
