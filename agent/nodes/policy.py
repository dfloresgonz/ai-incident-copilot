from typing import Dict, Any, List
from pydantic import BaseModel, Field
from agent.state import IncidentState

# Strict catalog of authorized AWS Systems Manager automation runbooks
ALLOWED_RUNBOOKS = {
    "AWS-RestartECSService",
    "AWS-RollbackDeployment",
    "AWS-ScaleECSService"
}

class RemediationPlanSchema(BaseModel):
    service_name: str
    runbook: str
    parameters: Dict[str, Any]
    requires_canary: bool = True

def policy_engine_node(state: IncidentState) -> Dict[str, Any]:
    """
    Policy Engine: Deterministic validation gate.
    Ensures LLM proposals conform to allowed SSM documents and least-privilege bounds.
    """
    recommended_runbook = state.get("recommended_runbook")
    violations: List[str] = []
    
    if recommended_runbook not in ALLOWED_RUNBOOKS:
        violations.append(f"Proposed runbook '{recommended_runbook}' is not in the authorized catalog.")
    
    is_approved = len(violations) == 0
    
    return {
        "is_policy_approved": is_approved,
        "policy_violations": violations
    }
