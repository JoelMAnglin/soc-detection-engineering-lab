import unittest

from soclab.detections import RULES


class DetectionTests(unittest.TestCase):
    def test_encoded_powershell_from_word(self):
        event = {
            "source": "crowdstrike", "event_type": "ProcessRollup2",
            "process_name": "powershell.exe", "parent_process": "WINWORD.EXE",
            "command_line": "powershell.exe -EncodedCommand SQBFAFgA",
        }
        self.assertTrue(next(x for x in RULES if x["id"] == "SOC-EDR-001")["match"](event))

    def test_benign_powershell_does_not_match(self):
        event = {
            "source": "crowdstrike", "event_type": "ProcessRollup2",
            "process_name": "powershell.exe", "parent_process": "explorer.exe",
            "command_line": "powershell.exe Get-Date",
        }
        self.assertFalse(next(x for x in RULES if x["id"] == "SOC-EDR-001")["match"](event))

    def test_proofpoint_delivered_phish(self):
        event = {
            "source": "proofpoint", "event_type": "message", "severity": "high",
            "threat_type": "credential_phishing", "delivery_status": "delivered",
        }
        self.assertTrue(next(x for x in RULES if x["id"] == "SOC-EMAIL-001")["match"](event))


if __name__ == "__main__":
    unittest.main()

