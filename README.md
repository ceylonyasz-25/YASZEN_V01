# YASZEN_V01 — Human-Serving Intelligence Prototype

> *"Empowering conscious humans in a world of intelligent machines."*

## What Is This?

YASZEN_V01 is a physical + software deliberation system that **augments human decision-making** rather than replacing human agency. It combines:

- An **Arduino-powered physical console** (LEDs + tactile buttons in a cardboard enclosure)
- A **Python Cognitive Friction Engine** that detects cognitive biases, applies ethical constraints, and generates Socratic challenges
- A **Decision Journal** that logs every deliberation for future reflection

## Philosophy

Rooted in Buddhist cognitive epistemology:
- **Sati Protocol** — Mindful reflection pause before any output
- **Cetanā Gate** — The machine refuses to steal your volition; you must claim every decision
- **Paṭicca Audit** — Second-order impact analysis (dependent origination)

## Quick Start

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Flash Arduino
Open `arduino/yaszen_console/yaszen_console.ino` in Arduino IDE and upload.

### 3. Run YASZEN
```bash
python main.py
```

The system auto-detects Arduino. If no hardware is connected, it runs in software-only mode with keyboard input.

## Project Structure

```
Body_v01/
├── arduino/yaszen_console/
│   └── yaszen_console.ino       ← Arduino firmware
├── yaszen/
│   ├── __init__.py
│   ├── bridge.py                ← Serial communication
│   ├── engine.py                ← Cognitive Friction Engine
│   ├── journal.py               ← Decision logging
│   └── config/
│       └── ethical_rules.yaml   ← Ethical constraints & bias rules
├── main.py                      ← Entry point
├── requirements.txt
└── README.md
```

## License

Built with intention by Yasuni Thashmika · YASZEN · Negombo, Sri Lanka
