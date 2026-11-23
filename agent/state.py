from typing import TypedDict, List, Dict, Any, Optional

class IncidentState(TypedDict):
    """
    Global state schema managed across the LangGraph multi-agent lifecycle.
    """
    # Ingress Telemetry
    incident_id: str
    service_name: str
    raw_alerts: List[Dict[str, Any]]
    
    # Triage Agent (Claude Haiku 5.5)
    severity: Optional[str]  # P1, P2, P3, P4
    is_flapping: bool
    triage_summary: Optional[str]
    
    # Telemetry Agent (MCP CloudWatch)
    cloudwatch_metrics: Dict[str, Any]
    error_logs: List[str]
    
    # Code Agent (MCP GitHub)
    recent_commits: List[Dict[str, Any]]
    diff_analysis: Optional[str]
    
    # Memory Agent (PostgreSQL Hybrid RAG)
    similar_incidents: List[Dict[str, Any]]
    
    # RCA Lead Agent (Claude Sonnet 5.5)
    root_cause_hypothesis: Optional[str]
    recommended_runbook: Optional[str]
    runbook_parameters: Dict[str, Any]
    
    # Policy Engine
    is_policy_approved: bool
    policy_violations: List[str]
    
    # Human-in-the-Loop & Execution
    slack_thread_ts: Optional[str]
    execution_status: Optional[str]
