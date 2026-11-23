import json
from langgraph.graph import StateGraph, END
from agent.state import IncidentState
from agent.nodes.triage import triage_agent_node
from agent.nodes.telemetry import telemetry_agent_node
from agent.nodes.code import code_agent_node
from agent.nodes.memory import memory_agent_node
from agent.nodes.rca_lead import rca_lead_agent_node
from agent.nodes.policy import policy_engine_node

def should_investigate(state: IncidentState) -> str:
    """Conditional edge: halts workflow if alarm is determined to be flapping."""
    if state.get("is_flapping", False):
        return "end"
    return "telemetry"

def build_incident_graph() -> StateGraph:
    """
    Constructs the multi-agent incident response state graph.
    """
    workflow = StateGraph(IncidentState)
    
    # Register Agent Nodes
    workflow.add_node("triage", triage_agent_node)
    workflow.add_node("telemetry", telemetry_agent_node)
    workflow.add_node("code", code_agent_node)
    workflow.add_node("memory", memory_agent_node)
    workflow.add_node("rca_lead", rca_lead_agent_node)
    workflow.add_node("policy", policy_engine_node)
    
    # Set Entry Point
    workflow.set_entry_point("triage")
    
    # Graph Edges
    workflow.add_conditional_edges(
        "triage",
        should_investigate,
        {
            "telemetry": "telemetry",
            "end": END
        }
    )
    workflow.add_edge("telemetry", "code")
    workflow.add_edge("code", "memory")
    workflow.add_edge("memory", "rca_lead")
    workflow.add_edge("rca_lead", "policy")
    workflow.add_edge("policy", END)
    
    return workflow.compile()

if __name__ == "__main__":
    app = build_incident_graph()
    
    # Simulation Event Input
    initial_event: IncidentState = {
        "incident_id": "inc-live-8921",
        "service_name": "checkout-service",
        "raw_alerts": [
            {"alarm": "HighErrorRate5xx", "status": "ALARM"},
            {"alarm": "TargetResponseTimeP99", "status": "ALARM"},
            {"alarm": "DatabaseConnectionLimit80Pct", "status": "ALARM"},
            {"alarm": "ContainerTaskFailures", "status": "ALARM"},
            {"alarm": "DeadlockCountExceeded", "status": "ALARM"},
            {"alarm": "APIGateway504BackendTimeout", "status": "ALARM"}
        ],
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
    
    print("Executing Multi-Agent Incident Response Graph...")
    result = app.invoke(initial_event)
    print("\n--- Final Multi-Agent Output ---")
    print(json.dumps(result, indent=2))
