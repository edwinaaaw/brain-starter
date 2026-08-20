import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "skills/brain-starter/scripts/session_store.py"
SPEC = importlib.util.spec_from_file_location("session_store", MODULE_PATH)
session_store = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(session_store)


def valid_event():
    return {
        "startedAt": "2026-08-17T09:30:00+08:00",
        "inputMode": "voice",
        "taskClarity": "clear",
        "taskType": "work",
        "resistance": "task_too_large",
        "aiLevel": 3,
        "connectorsUsed": ["gmail"],
        "firstAction": "review_draft",
        "startedWithinThreeMinutes": True,
        "completedTenMinuteBlock": False,
        "continuedAfterBlock": False,
        "resistanceBefore": 4,
        "resistanceAfter": 2,
    }


class SessionStoreTests(unittest.TestCase):
    def test_valid_event_is_normalized(self):
        event = session_store.validate_event(valid_event())
        self.assertEqual(event["aiLevel"], 3)
        self.assertEqual(event["connectorsUsed"], ["gmail"])
        self.assertEqual(event["facility"], "workbench")
        self.assertEqual(event["momentumEarned"], 2)

    def test_momentum_rewards_real_action_not_planning(self):
        event = valid_event()
        event["startedWithinThreeMinutes"] = False
        self.assertEqual(session_store.validate_event(event)["momentumEarned"], 0)

        event["startedWithinThreeMinutes"] = True
        event["completedTenMinuteBlock"] = True
        event["continuedAfterBlock"] = True
        self.assertEqual(session_store.validate_event(event)["momentumEarned"], 5)

    def test_summary_aggregates_momentum_and_facilities(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "events.jsonl"
            first = valid_event()
            second = valid_event()
            second["taskType"] = "personal"
            second["completedTenMinuteBlock"] = True
            session_store.append_event(first, path)
            session_store.append_event(second, path)

            summary = session_store.summarize(path)
            self.assertEqual(summary["totalMomentum"], 6)
            self.assertEqual(summary["starts"], 2)
            self.assertEqual(summary["facilities"], {"life_dock": 4, "workbench": 2})

    def test_unknown_or_private_fields_are_rejected(self):
        for field in ("emailBody", "voiceTranscript", "accessToken", "notes"):
            with self.subTest(field=field):
                event = valid_event()
                event[field] = "private"
                with self.assertRaises(ValueError):
                    session_store.validate_event(event)

    def test_invalid_values_are_rejected(self):
        mutations = {
            "inputMode": "camera",
            "taskClarity": "maybe",
            "aiLevel": 6,
            "resistanceBefore": 0,
            "completedTenMinuteBlock": "yes",
        }
        for field, value in mutations.items():
            with self.subTest(field=field):
                event = valid_event()
                event[field] = value
                with self.assertRaises(ValueError):
                    session_store.validate_event(event)

    def test_append_writes_jsonl_with_private_permissions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "events.jsonl"
            returned = session_store.append_event(valid_event(), path)
            self.assertEqual(returned, path)
            stored = json.loads(path.read_text(encoding="utf-8").strip())
            self.assertEqual(stored["taskType"], "work")
            self.assertEqual(os.stat(path).st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()
