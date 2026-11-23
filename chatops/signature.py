import hmac
import hashlib
import time

def verify_slack_signature(signing_secret: str, request_body: str, timestamp: str, signature: str) -> bool:
    """
    Verifies incoming Slack interactive webhooks using HMAC SHA-256.
    Protects against replay attacks with a 5-minute threshold.
    """
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False
        
    sig_basestring = f"v0:{timestamp}:{request_body}".encode("utf-8")
    computed_sig = "v0=" + hmac.new(
        signing_secret.encode("utf-8"),
        sig_basestring,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(computed_sig, signature)
