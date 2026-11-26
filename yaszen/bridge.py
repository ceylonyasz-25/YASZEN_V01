"""
YASZEN Arduino Bridge
Handles serial communication between Python intelligence and physical console.
"""
import serial
import serial.tools.list_ports
import time
import threading


class YaszenBridge:
    """Bidirectional bridge between Python and the YASZEN physical console."""

    def __init__(self, port=None, baud=9600):
        self.port = port or self._find_arduino()
        self.baud = baud
        self.ser = None
        self.button_callbacks = {}
        self._listening = False

    def _find_arduino(self):
        """Auto-detect Arduino COM port."""
        ports = serial.tools.list_ports.comports()
        for p in ports:
            desc = p.description.lower()
            if any(kw in desc for kw in ['arduino', 'ch340', 'cp210', 'ftdi', 'usb-serial', 'usb serial']):
                print(f"[Bridge] Found Arduino on {p.device} ({p.description})")
                return p.device

        # Fallback — show available ports and ask
        print("[Bridge] No Arduino auto-detected. Available ports:")
        for p in ports:
            print(f"  {p.device}: {p.description}")
        if not ports:
            print("  (No serial ports found. Is Arduino plugged in?)")
            return None
        return input("[Bridge] Enter COM port manually (e.g., COM3): ").strip()

    def connect(self):
        """Establish serial connection."""
        if not self.port:
            return False
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=0.1)
            time.sleep(2)  # Wait for Arduino reset after serial open

            # Wait for YASZEN_READY signal
            start = time.time()
            while time.time() - start < 5:
                line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                if line == "YASZEN_READY":
                    print("[Bridge] ✓ Console connected and ready.")
                    return True

            print("[Bridge] ✓ Connected (no ready signal — may already be running).")
            return True
        except Exception as e:
            print(f"[Bridge] ✗ Connection failed: {e}")
            return False

    def send(self, command):
        """Send a command string to Arduino."""
        if self.ser and self.ser.is_open:
            self.ser.write(f"{command}\n".encode())

    def on_button(self, button_name, callback):
        """Register a callback for a specific button press event."""
        self.button_callbacks[button_name] = callback

    def start_listening(self):
        """Start background thread to listen for button presses."""
        self._listening = True
        thread = threading.Thread(target=self._listen_loop, daemon=True)
        thread.start()

    def _listen_loop(self):
        """Background listener for Arduino button messages."""
        while self._listening:
            try:
                if self.ser and self.ser.in_waiting:
                    line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if line.startswith("BTN:"):
                        button = line.split(":")[1]
                        if button in self.button_callbacks:
                            self.button_callbacks[button]()
            except Exception:
                time.sleep(0.05)

    def stop(self):
        """Clean shutdown."""
        self._listening = False
        self.send("ALL_OFF")
        time.sleep(0.1)
        if self.ser and self.ser.is_open:
            self.ser.close()
        print("[Bridge] Console disconnected.")

    # --- Convenience methods ---
    def reflect(self, on=True):
        """Control the yellow reflection/contemplation LED."""
        self.send("REFLECT_ON" if on else "REFLECT_OFF")

    def ethics_alert(self, on=True):
        """Control the red ethical alert LED."""
        self.send("ETHICS_ON" if on else "ETHICS_OFF")

    def agency_confirmed(self, on=True):
        """Control the green human agency LED."""
        self.send("AGENCY_ON" if on else "AGENCY_OFF")

    def clear(self):
        """Turn off all LEDs."""
        self.send("ALL_OFF")
