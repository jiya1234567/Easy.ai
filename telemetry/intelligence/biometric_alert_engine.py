"""
BiometricAlertEngine — OMEGA-CORE Health Alert Module
Sends Email and SMS alerts when biometric stress thresholds are breached.
Uses smtplib (email) and Twilio (SMS).
"""
import smtplib
import os
import json
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Auto-load .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"), override=False)
except ImportError:
    pass  # dotenv not installed; fall back to system env vars

# ── Thresholds ────────────────────────────────────────────────────────────────
THRESHOLDS = {
    "bp_systolic": {"warning": 130, "critical": 160, "low": 90},
    "glucose":     {"warning": 140, "critical": 200, "low": 70},
    "pulse":       {"warning": 100, "critical": 130, "low": 50},
    "spo2":        {"warning": 94,  "critical": 90,  "low": None},   # Low is bad for SpO2
}

ALERT_LOG_PATH = "reports/biometric_alert_log.json"

# ── Core Engine ───────────────────────────────────────────────────────────────
class BiometricAlertEngine:
    """
    Evaluates biometric readings, classifies risk level,
    and dispatches Email + SMS alerts when thresholds are breached.
    """

    def __init__(self, owner_name="AJ Phillips"):
        self.owner = owner_name
        self.smtp_host    = os.environ.get("ALERT_SMTP_HOST", "smtp-mail.outlook.com")
        self.smtp_port    = int(os.environ.get("ALERT_SMTP_PORT", 587))
        self.smtp_user    = os.environ.get("ALERT_EMAIL_FROM", "")
        self.smtp_pass    = os.environ.get("ALERT_EMAIL_PASS", "")
        self.alert_to     = os.environ.get("ALERT_EMAIL_TO",   "")
        self.alert_log    = self._load_log()

    # ── Evaluate ──────────────────────────────────────────────────────────────
    def evaluate(self, bp: str, glucose: float, pulse: float, spo2: float = 98.0) -> dict:
        """
        bp format: "120/80"
        Returns: {level: "OK|WARNING|CRITICAL", breaches: [...], message: str}
        """
        try:
            systolic = int(bp.split("/")[0])
        except Exception:
            systolic = 120

        breaches = []
        level = "OK"

        checks = [
            ("Blood Pressure", systolic, THRESHOLDS["bp_systolic"]),
            ("Glucose",        glucose,  THRESHOLDS["glucose"]),
            ("Pulse",          pulse,    THRESHOLDS["pulse"]),
        ]

        for name, val, thr in checks:
            if val >= thr["critical"]:
                breaches.append({"metric": name, "value": val, "severity": "CRITICAL"})
                level = "CRITICAL"
            elif val >= thr["warning"]:
                if level != "CRITICAL":
                    level = "WARNING"
                breaches.append({"metric": name, "value": val, "severity": "WARNING"})
            elif thr.get("low") and val <= thr["low"]:
                breaches.append({"metric": name, "value": val, "severity": "LOW"})
                if level != "CRITICAL":
                    level = "WARNING"

        # SpO2 — lower is worse
        if spo2 <= THRESHOLDS["spo2"]["critical"]:
            breaches.append({"metric": "SpO2", "value": spo2, "severity": "CRITICAL"})
            level = "CRITICAL"
        elif spo2 <= THRESHOLDS["spo2"]["warning"]:
            breaches.append({"metric": "SpO2", "value": spo2, "severity": "WARNING"})
            if level != "CRITICAL":
                level = "WARNING"

        ts  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = self._build_message(level, breaches, bp, glucose, pulse, spo2, ts)

        result = {
            "timestamp": ts,
            "owner":     self.owner,
            "level":     level,
            "breaches":  breaches,
            "message":   msg,
            "vitals":    {"bp": bp, "glucose": glucose, "pulse": pulse, "spo2": spo2}
        }

        self.alert_log.append(result)
        self._save_log()
        return result

    # ── Email ─────────────────────────────────────────────────────────────────
    def send_email(self, result: dict) -> str:
        """
        Send via SendGrid API (recommended — free 100/day, no OAuth needed).
        Falls back to Gmail SMTP if SENDGRID_API_KEY not set.
        Note: Outlook personal SMTP is permanently blocked by Microsoft (OAuth only).
        """
        sg_key   = os.environ.get("SENDGRID_API_KEY", "")
        email_to = self.alert_to
        email_fr = self.smtp_user

        if not email_to:
            return "⚠️ Email not configured. Open sidebar → 🔑 Alert Credentials → set your email."

        subject = f"🚨 OMEGA-CORE BIOMETRIC ALERT [{result['level']}] — {result['timestamp']}"
        body    = result["message"]

        # ── Option A: SendGrid API (recommended) ──
        if sg_key:
            try:
                import urllib.request, urllib.error
                import json as _json
                payload = _json.dumps({
                    "personalizations": [{"to": [{"email": email_to}]}],
                    "from": {"email": email_fr or "noreply@omegacore.ai", "name": "OMEGA-CORE"},
                    "subject": subject,
                    "content": [{"type": "text/plain", "value": body}]
                }).encode()
                req = urllib.request.Request(
                    "https://api.sendgrid.com/v3/mail/send",
                    data=payload,
                    headers={"Authorization": f"Bearer {sg_key}",
                             "Content-Type": "application/json"}
                )
                urllib.request.urlopen(req, timeout=10)
                return f"✅ Email sent via SendGrid to {email_to}"
            except Exception as e:
                return f"❌ SendGrid failed: {e}"

        # ── Option B: Gmail SMTP fallback ──
        smtp_host = os.environ.get("ALERT_SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.environ.get("ALERT_SMTP_PORT", 587))
        if not self.smtp_user or not self.smtp_pass:
            return ("⚠️ Email not configured. Choose one option:\n"
                    "  Option 1 (Recommended): Get free SendGrid API key at sendgrid.com → "
                    "enter SENDGRID_API_KEY in sidebar credentials.\n"
                    "  Option 2: Use a Gmail account — set ALERT_EMAIL_FROM=you@gmail.com, "
                    "ALERT_EMAIL_PASS=gmail-app-password (16 chars from myaccount.google.com/apppasswords), "
                    "ALERT_SMTP_HOST=smtp.gmail.com.\n"
                    "  ⚠️ Outlook SMTP is permanently blocked by Microsoft — use SendGrid or Gmail instead.")
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"]    = self.smtp_user
            msg["To"]      = email_to
            msg.attach(MIMEText(body, "plain"))
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.sendmail(self.smtp_user, email_to, msg.as_string())
            return f"✅ Email sent via {smtp_host} to {email_to}"
        except Exception as e:
            return f"❌ Email failed: {e}"

    # ── SMS via Twilio ────────────────────────────────────────────────────────
    def send_sms(self, result: dict, smart_summary: str = None) -> str:
        twilio_sid   = os.environ.get("TWILIO_ACCOUNT_SID", "")
        twilio_token = os.environ.get("TWILIO_AUTH_TOKEN",  "")
        from_num     = os.environ.get("TWILIO_FROM_NUMBER", "")
        to_num       = os.environ.get("TWILIO_TO_NUMBER",   "")

        if not all([twilio_sid, twilio_token, from_num, to_num]):
            return "⚠️ SMS not configured. Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, TWILIO_TO_NUMBER."

        try:
            from twilio.rest import Client
            client  = Client(twilio_sid, twilio_token)
            
            if smart_summary:
                sms_body = smart_summary
            else:
                sms_body = (
                    f"OMEGA-CORE ALERT [{result['level']}]\n"
                    f"{result['owner']} | {result['timestamp']}\n"
                    + "\n".join([f"• {b['metric']}: {b['value']} ({b['severity']})" for b in result["breaches"]])
                    + f"\nAction: {result['message'].split(chr(10))[0]}"
                )
                
            message = client.messages.create(body=sms_body, from_=from_num, to=to_num)
            return f"✅ SMS sent (SID: {message.sid})"
        except ImportError:
            return "⚠️ Twilio not installed. Run: pip install twilio"
        except Exception as e:
            return f"❌ SMS failed: {e}"

    def generate_smart_summary(self, result: dict, provider="gemini", api_key=None) -> str:
        """
        Uses LLM to generate a concise, professional medical summary for SMS/Email.
        """
        if not api_key:
            return None
            
        prompt = f"""
        You are OMEGA-CORE MEDICAL LIAISON. Generate a concise, professional SMS alert for the following biometric breach:
        
        OWNER: {result['owner']}
        STATUS: {result['level']}
        VITALS: {json.dumps(result['vitals'])}
        BREACHES: {json.dumps(result['breaches'])}
        
        REQUIREMENTS:
        - Max 160 characters.
        - Include current status and primary risk.
        - Provide one clear action step.
        - Maintain a professional, urgent but calm tone.
        """
        
        try:
            if provider == "gemini":
                from google import genai
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )
                return response.text.strip()
            elif provider == "mistral":
                from mistralai.client import Mistral
                client = Mistral(api_key=api_key)
                response = client.chat.complete(
                    model="mistral-large-latest",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Smart Summary failed: {e}")
            return None

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _build_message(self, level, breaches, bp, glucose, pulse, spo2, ts) -> str:
        lines = [
            f"OMEGA-CORE Biometric Alert — {level}",
            f"Owner : {self.owner}",
            f"Time  : {ts}",
            f"",
            f"VITALS:",
            f"  Blood Pressure : {bp}",
            f"  Glucose        : {glucose} mg/dL",
            f"  Pulse          : {pulse} BPM",
            f"  SpO2           : {spo2}%",
            f"",
        ]
        if breaches:
            lines.append("THRESHOLD BREACHES:")
            for b in breaches:
                lines.append(f"  ⚠ {b['metric']} = {b['value']}  [{b['severity']}]")
        else:
            lines.append("All vitals within normal range. No action required.")
        lines += [
            "",
            "ACTION: Review Samsung Galaxy Fit 3 / Samsung Health log.",
            "Powered by OMEGA-CORE v2.5 | Node-04 (Geneva)",
        ]
        return "\n".join(lines)

    def _load_log(self):
        if os.path.exists(ALERT_LOG_PATH):
            try:
                with open(ALERT_LOG_PATH) as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_log(self):
        os.makedirs("reports", exist_ok=True)
        with open(ALERT_LOG_PATH, "w") as f:
            json.dump(self.alert_log[-100:], f, indent=2)   # Keep last 100 entries

    def get_log(self):
        return self.alert_log


if __name__ == "__main__":
    engine = BiometricAlertEngine("AJ Phillips")
    # Simulate a critical stress test
    result = engine.evaluate(bp="180/110", glucose=210, pulse=135, spo2=88)
    print(json.dumps(result, indent=2))
