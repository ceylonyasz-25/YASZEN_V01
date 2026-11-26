"""
YASZEN Cognitive Friction Engine
The core differentiator — intercepts thinking, detects bias, injects reflection.

This is the intellectual heart of YASZEN: a module that sits between
human input and system output, applying deliberate cognitive friction
to encourage deeper, more conscious decision-making.
"""
import yaml
import random
from pathlib import Path


class CognitiveFrictionEngine:
    """Analyzes user propositions for cognitive biases and ethical concerns."""

    def __init__(self, rules_path=None):
        if rules_path is None:
            rules_path = Path(__file__).parent / "config" / "ethical_rules.yaml"

        with open(rules_path, 'r', encoding='utf-8') as f:
            self.rules = yaml.safe_load(f)

        self.session_log = []

    def analyze(self, proposition):
        """
        Full analysis pipeline.
        Returns a structured result with detected biases, ethical flags,
        Socratic prompts, and a reflection friction score.
        """
        result = {
            'proposition': proposition,
            'biases_detected': [],
            'ethical_flags': [],
            'reflection_score': 0.0,  # 0 = minimal friction, 1 = maximum friction
            'socratic_prompts': {},
            'should_refuse': False,
            'refusal_reason': None,
        }

        text_lower = proposition.lower()

        # 1. Detect cognitive biases via keyword triggers
        for bias in self.rules.get('cognitive_biases', []):
            for keyword in bias['keywords']:
                if keyword.lower() in text_lower:
                    result['biases_detected'].append({
                        'id': bias['id'],
                        'name': bias.get('name', bias['id']),
                        'trigger': keyword,
                        'challenge': bias['challenge'],
                    })
                    break  # One match per bias type is enough

        # 2. Check ethical refusal triggers
        autonomy_phrases = [
            'decide for me', 'just tell me what to do',
            'make the choice', 'you choose', 'you decide',
            'what should i do', 'tell me the answer',
        ]
        if any(phrase in text_lower for phrase in autonomy_phrases):
            result['should_refuse'] = True
            refusal = self._get_refusal('no_autonomous_decisions')
            result['refusal_reason'] = refusal

        harm_phrases = [
            'ignore the consequences', "doesn't matter who",
            'collateral damage', 'sacrifice them', 'who cares if',
        ]
        if any(phrase in text_lower for phrase in harm_phrases):
            result['ethical_flags'].append({
                'rule': 'no_harm_optimization',
                'message': self._get_refusal('no_harm_optimization'),
            })

        deception_phrases = [
            'make it sound like', 'hide the fact', 'spin this',
            'mislead', 'trick them', 'they won\'t notice',
        ]
        if any(phrase in text_lower for phrase in deception_phrases):
            result['ethical_flags'].append({
                'rule': 'no_deception',
                'message': self._get_refusal('no_deception'),
            })

        responsibility_phrases = [
            'not my fault', 'blame the algorithm', 'the ai decided',
            'it\'s not on me', 'the system chose',
        ]
        if any(phrase in text_lower for phrase in responsibility_phrases):
            result['ethical_flags'].append({
                'rule': 'no_responsibility_transfer',
                'message': self._get_refusal('no_responsibility_transfer'),
            })

        # 3. Calculate reflection friction score
        friction_points = (
            len(result['biases_detected']) * 0.2 +
            len(result['ethical_flags']) * 0.3 +
            (0.4 if result['should_refuse'] else 0)
        )
        result['reflection_score'] = min(friction_points, 1.0)

        # 4. Select contextual Socratic prompts
        templates = self.rules.get('socratic_templates', {})
        for category in ['challenge', 'impact', 'sovereignty']:
            pool = templates.get(category, [])
            count = min(2, len(pool))
            result['socratic_prompts'][category] = random.sample(pool, count) if count > 0 else []

        # Log this analysis
        self.session_log.append(result)

        return result

    def _get_refusal(self, refusal_id):
        """Look up a refusal response by ID."""
        for r in self.rules.get('refusals', []):
            if r['id'] == refusal_id:
                return r['response']
        return "This requires deeper reflection before proceeding."

    def format_analysis(self, result):
        """Format analysis result for terminal display."""
        lines = []

        # Biases
        if result['biases_detected']:
            lines.append("")
            lines.append("[YASZEN · Bias Detection]")
            for bias in result['biases_detected']:
                lines.append(f"  ⚠ {bias['name']} detected")
                lines.append(f"    Trigger phrase: \"{bias['trigger']}\"")
                lines.append(f"    → {bias['challenge']}")

        # Ethical flags
        if result['ethical_flags']:
            lines.append("")
            lines.append("[YASZEN · Ethical Alert]")
            for flag in result['ethical_flags']:
                lines.append(f"  ● {flag['message']}")

        # Refusal
        if result['should_refuse']:
            lines.append("")
            lines.append("[YASZEN · Cetanā Gate — REFUSAL]")
            lines.append(f"  ✋ {result['refusal_reason']}")

        # Reflection score
        score = result['reflection_score']
        if score > 0.6:
            level = "HIGH — significant cognitive friction applied"
        elif score > 0.3:
            level = "MODERATE — some biases or concerns detected"
        else:
            level = "LOW — proceed with standard reflection"
        lines.append("")
        lines.append(f"[Reflection Score: {score:.0%} — {level}]")

        return '\n'.join(lines)

    def get_session_summary(self):
        """Summary of all deliberations in this session."""
        total = len(self.session_log)
        biases = sum(len(r['biases_detected']) for r in self.session_log)
        refusals = sum(1 for r in self.session_log if r['should_refuse'])
        avg_score = (
            sum(r['reflection_score'] for r in self.session_log) / total
            if total > 0 else 0
        )
        return {
            'total_deliberations': total,
            'total_biases_detected': biases,
            'total_refusals': refusals,
            'average_reflection_score': round(avg_score, 2),
        }
