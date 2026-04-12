class MitreMapper:
    """
    Maps synthetic cybersecurity alerts to real-world MITRE ATT&CK techniques.
    """
    TECHNIQUES = {
        "DDoS": {
            "id": "T1498",
            "name": "Network Denial of Service",
            "description": "Adversaries may perform Network Denial of Service (DoS) attacks to degrade or block the availability of services.",
            "detection": "Monitor for unusual volume of network traffic and system performance degradation."
        },
        "BruteForce": {
            "id": "T1110",
            "name": "Brute Force",
            "description": "Adversaries may use brute force techniques to gain access to accounts.",
            "detection": "Monitor for high frequency of failed login attempts."
        },
        "Privilege Escalation": {
            "id": "T1068",
            "name": "Exploitation for Privilege Escalation",
            "description": "Adversaries may exploit software vulnerabilities to elevate their privileges.",
            "detection": "Monitor for unusual process executions or system configuration changes."
        },
        "Lateral Movement": {
            "id": "T1021",
            "name": "Remote Services",
            "description": "Adversaries may use valid credentials to move laterally within an environment.",
            "detection": "Monitor for unusual login patterns across different systems."
        },
        "Exfiltration": {
            "id": "T1048",
            "name": "Exfiltration Over Alternative Protocol",
            "description": "Adversaries may exfiltrate data over protocols other than the primary command and control channel.",
            "detection": "Monitor for large volume data transfers to external IP addresses."
        }
    }

    @classmethod
    def get_mitre_context(cls, attack_type):
        """
        Returns MITRE context for a given attack type.
        """
        return cls.TECHNIQUES.get(attack_type, {
            "id": "Unknown",
            "name": "Unknown Technique",
            "description": "No MITRE mapping found for this attack type.",
            "detection": "General anomaly detection recommended."
        })

if __name__ == "__main__":
    mapper = MitreMapper()
    print(mapper.get_mitre_context("DDoS"))
