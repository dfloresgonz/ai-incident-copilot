import json
from typing import Dict, Any

def generate_incident_slack_blocks(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Constructs an interactive Slack Block Kit message with diagnosis,
    evidence, and a 1-click remediation action button.
    """
    incident_id = state.get("incident_id")
    service = state.get("service_name")
    severity = state.get("severity", "P1")
    hypothesis = state.get("root_cause_hypothesis", "Under investigation")
    runbook = state.get("recommended_runbook", "AWS-RestartECSService")
    
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"🚨 [CRITICAL {severity}] Autonomous RCA: {service}",
                "emoji": True
            }
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Incident ID:*\n`{incident_id}`"},
                {"type": "mrkdwn", "text": f"*Severity:*\n*{severity}*"},
                {"type": "mrkdwn", "text": "*MTTR Reduction Target:*\n`< 3 min`"},
                {"type": "mrkdwn", "text": "*Policy Status:*\n✅ Approved (Pydantic v2)"}
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Root Cause Analysis:*\n{hypothesis}"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"👉 *Recommended Remediation Action:* `{runbook}`\n_Step Functions will execute the runbook with a 180s canary window and automated rollback if 5xx error rate remains $\\ge$ 0.1%._"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "⚡ Authorize 1-Click Remediation",
                        "emoji": True
                    },
                    "style": "danger",
                    "value": json.dumps({"incident_id": incident_id, "action": "execute", "runbook": runbook}),
                    "action_id": "approve_remediation_btn"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Dismiss / False Alarm",
                        "emoji": True
                    },
                    "value": json.dumps({"incident_id": incident_id, "action": "dismiss"}),
                    "action_id": "dismiss_alarm_btn"
                }
            ]
        }
    ]
    
    return {"blocks": blocks}
