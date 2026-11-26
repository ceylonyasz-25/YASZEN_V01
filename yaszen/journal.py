"""
YASZEN Decision Journal
Persistent log of all deliberations for future reflection and pattern analysis.
"""
import json
import time
from pathlib import Path


class DecisionJournal:
    """Logs every deliberation session to a JSONL file."""

    def __init__(self, path=None):
        self.path = Path(path or "decisions.jsonl")

    def log(self, proposition, analysis, buttons_pressed, final_action="decided"):
        """Record a completed deliberation."""
        entry = {
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'proposition': proposition,
            'biases_found': [b['id'] for b in analysis.get('biases_detected', [])],
            'ethical_flags': [f['rule'] for f in analysis.get('ethical_flags', [])],
            'reflection_score': analysis.get('reflection_score', 0),
            'refused': analysis.get('should_refuse', False),
            'buttons_pressed': buttons_pressed,
            'outcome': final_action,
        }

        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')

        return entry

    def read_all(self):
        """Read all past journal entries."""
        entries = []
        if self.path.exists():
            with open(self.path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        entries.append(json.loads(line))
        return entries

    def summary(self):
        """Print a human-readable summary of the decision journal."""
        entries = self.read_all()
        if not entries:
            return "No decisions logged yet."

        total = len(entries)
        biases = sum(len(e.get('biases_found', [])) for e in entries)
        refusals = sum(1 for e in entries if e.get('refused'))
        avg_score = sum(e.get('reflection_score', 0) for e in entries) / total

        lines = [
            f"Decision Journal — {total} deliberation(s) logged",
            f"  Biases caught: {biases}",
            f"  Refusals triggered: {refusals}",
            f"  Avg reflection score: {avg_score:.0%}",
        ]
        return '\n'.join(lines)
