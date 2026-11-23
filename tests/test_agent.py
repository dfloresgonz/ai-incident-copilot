import pytest
from agent.nodes.triage import triage_agent_node
from agent.nodes.policy import policy_engine_node
from agent.state import IncidentState

def test_triage_p1_classification():
    state: IncidentState = {
        "incident_id": "test-001",
        "service_name": "checkout-service",
        "raw_alerts": [{"alarm": "HTTP 504 Gateway Timeout"}] * 6,
        "severity": None,
        "is_flapping": False,
        "triage_summary": None,
        "cloudwatch_metrics": {},
        "error_logs": [],
        "recent_commits": [],
        "diff_analysis": None,
        "similar_incidents": [],
        "root_cause_hypothesis": None,
        "recommended_runbook": None,
        "runbook_parameters": {},
        "is_policy_approved": False,
        "policy_violations": [],
        "slack_thread_ts": None,
        "execution_status": None
    }
    
    result = triage_agent_node(state)
    assert result["severity"] == "P1"
    assert result["is_flapping"] is False

def test_policy_engine_validation():
    valid_state: IncidentState = {
        "recommended_runbook": "AWS-RestartECSService"
    }
    invalid_state: IncidentState = {
        "recommended_runbook": "rm -rf /"
    }
    
    valid_res = policy_engine_node(valid_state)
    assert valid_res["is_policy_approved"] is True
    
    invalid_res = policy_engine_node(invalid_state)
    assert invalid_res["is_policy_approved"] is False
    assert len(invalid_res["policy_violations"]) > 0
