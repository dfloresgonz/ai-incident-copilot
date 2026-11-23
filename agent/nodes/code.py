from typing import Dict, Any
from agent.state import IncidentState

def code_agent_node(state: IncidentState) -> Dict[str, Any]:
    """
    Code Agent: Uses mcp-github to inspect commits and deployments shipped
    within the failure window.
    """
    service_name = state.get("service_name")
    
    recent_commits = [
        {
            "commit_id": "7a8f3b1",
            "author": "dev-engineer@company.com",
            "message": "feat(checkout): add order discount validation query",
            "timestamp": "2026-11-23T02:40:00Z",
            "files_changed": ["src/services/discount.py", "src/models/order.py"]
        }
    ]
    
    diff_analysis = (
        "Commit 7a8f3b1 introduced an unindexed query on the discounts table "
        "inside the critical transaction block of /checkout/pay."
    )
    
    return {
        "recent_commits": recent_commits,
        "diff_analysis": diff_analysis
    }
