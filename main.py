"""
YASZEN_V01 — Human-Serving Intelligence Console
Main entry point for the deliberation system.

Run: python main.py
"""
from yaszen.bridge import YaszenBridge
from yaszen.engine import CognitiveFrictionEngine
from yaszen.journal import DecisionJournal
import time
import threading


# Shared state for button communication across threads
waiting_for_button = threading.Event()
last_button = [None]


BANNER = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              Y A S Z E N _ V 0 1                         ║
║                                                          ║
║      Human-Serving Intelligence · Deliberation Console   ║
║                                                          ║
║   "Empowering conscious humans in a world of             ║
║    intelligent machines"                                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""


def main():
    print(BANNER)

    # Initialize components
    engine = CognitiveFrictionEngine()
    journal = DecisionJournal()

    # Try connecting to physical console
    print("[System] Searching for YASZEN physical console...")
    bridge = YaszenBridge()
    hardware_connected = bridge.connect()

    if not hardware_connected:
        print("[System] Running in SOFTWARE-ONLY mode (keyboard input).")
        print("         Connect Arduino and restart for full physical experience.")
        bridge = None
    
    print()

    # Register button callbacks
    def on_challenge():
        last_button[0] = "CHALLENGE"
        waiting_for_button.set()

    def on_impact():
        last_button[0] = "IMPACT"
        waiting_for_button.set()

    def on_decide():
        last_button[0] = "DECIDE"
        waiting_for_button.set()

    if bridge:
        bridge.on_button("CHALLENGE", on_challenge)
        bridge.on_button("IMPACT", on_impact)
        bridge.on_button("DECIDE", on_decide)
        bridge.start_listening()

    try:
        while True:
            # ═══════════════════════════════════════
            # INPUT LAYER
            # ═══════════════════════════════════════
            print("\n" + "─" * 56)
            proposition = input("[You] Enter your proposition or dilemma:\n> ").strip()

            if proposition.lower() in ('exit', 'quit', 'q'):
                break

            if not proposition:
                continue

            buttons_pressed = []

            # ═══════════════════════════════════════
            # REFLECTION LAYER (Sati Protocol)
            # ═══════════════════════════════════════
            if bridge:
                bridge.clear()
                bridge.reflect(on=True)

            print(f"\n[YASZEN · Sati Protocol] Contemplating...")
            time.sleep(2)

            # ═══════════════════════════════════════
            # COGNITIVE FRICTION ENGINE
            # ═══════════════════════════════════════
            analysis = engine.analyze(proposition)
            formatted = engine.format_analysis(analysis)

            if bridge:
                bridge.reflect(on=False)
                # Red LED if biases or ethical issues found
                if analysis['biases_detected'] or analysis['ethical_flags'] or analysis['should_refuse']:
                    bridge.ethics_alert(on=True)

            print(formatted)

            # ═══════════════════════════════════════
            # INTERACTIVE DELIBERATION
            # ═══════════════════════════════════════
            print(f"\n[YASZEN · Cetanā Gate] This system will NOT decide for you.")
            print(f"─" * 56)

            if bridge:
                # Physical console mode
                print(f"  Button 1 → CHALLENGE : Question your assumptions")
                print(f"  Button 2 → IMPACT    : Examine ripple effects")
                print(f"  Button 3 → DECIDE    : Claim sovereignty over this choice")

                decided = False
                while not decided:
                    waiting_for_button.clear()
                    last_button[0] = None
                    waiting_for_button.wait()

                    btn = last_button[0]
                    buttons_pressed.append(btn)

                    if btn == "CHALLENGE":
                        bridge.ethics_alert(on=True)
                        prompts = analysis['socratic_prompts'].get('challenge', [])
                        print(f"\n[YASZEN · Socratic Challenge]")
                        for p in prompts:
                            print(f"  → {p}")
                        print(f"\n  (Press another button to continue)")

                    elif btn == "IMPACT":
                        prompts = analysis['socratic_prompts'].get('impact', [])
                        print(f"\n[YASZEN · Paṭicca Audit — Ripple Effects]")
                        for p in prompts:
                            print(f"  → {p}")
                        print(f"\n  (Press another button to continue)")

                    elif btn == "DECIDE":
                        decided = True

            else:
                # Software-only fallback mode
                print(f"  Type 'c' → CHALLENGE : Question your assumptions")
                print(f"  Type 'i' → IMPACT    : Examine ripple effects")
                print(f"  Type 'd' → DECIDE    : Claim sovereignty")

                decided = False
                while not decided:
                    choice = input("\n  [c/i/d] > ").strip().lower()

                    if choice == 'c':
                        buttons_pressed.append("CHALLENGE")
                        prompts = analysis['socratic_prompts'].get('challenge', [])
                        print(f"\n[YASZEN · Socratic Challenge]")
                        for p in prompts:
                            print(f"  → {p}")

                    elif choice == 'i':
                        buttons_pressed.append("IMPACT")
                        prompts = analysis['socratic_prompts'].get('impact', [])
                        print(f"\n[YASZEN · Paṭicca Audit — Ripple Effects]")
                        for p in prompts:
                            print(f"  → {p}")

                    elif choice == 'd':
                        buttons_pressed.append("DECIDE")
                        decided = True

            # ═══════════════════════════════════════
            # SOVEREIGNTY CONFIRMED
            # ═══════════════════════════════════════
            if bridge:
                bridge.clear()
                bridge.agency_confirmed(on=True)

            print(f"\n{'═' * 56}")
            print(f"  [YASZEN · Human Sovereignty Affirmed]")
            print(f"")
            print(f"  Reasoning augmented. Ethical friction applied.")
            print(f"  The choice belongs to you. The responsibility is yours.")
            print(f"")

            # Log to journal
            entry = journal.log(proposition, analysis, buttons_pressed)
            print(f"  Decision logged: {entry['timestamp']}")
            print(f"{'═' * 56}")

            time.sleep(3)
            if bridge:
                bridge.clear()

    except KeyboardInterrupt:
        print("\n\n[YASZEN] Session ended.")

    finally:
        # Session summary
        summary = engine.get_session_summary()
        if summary['total_deliberations'] > 0:
            print(f"\n{'─' * 56}")
            print(f"[Session Summary]")
            print(f"  Deliberations: {summary['total_deliberations']}")
            print(f"  Biases caught: {summary['total_biases_detected']}")
            print(f"  Refusals: {summary['total_refusals']}")
            print(f"  Avg reflection score: {summary['average_reflection_score']:.0%}")
            print(f"{'─' * 56}")

        if bridge:
            bridge.stop()

        print("[YASZEN] Stay conscious. The future belongs to aware humans.")


if __name__ == "__main__":
    main()
