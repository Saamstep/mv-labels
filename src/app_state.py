from src.ATEM import PyAtemMax
from src.LabelController import LabelController
from src.config_manager import ConfigManager


class AppState:
    def __init__(self):
        self.config = ConfigManager()
        host, port = self.config.get_connection_information()
        self.atem = PyAtemMax(host, port)
        self.labels = LabelController(self.atem, self.config)

    def reconnect_atem(self) -> tuple[bool, str]:
        host, port = self.config.get_connection_information()
        replacement = PyAtemMax(host, port)
        if not replacement.connect():
            return False, f"Saved config, but could not connect to ATEM at {host}:{port}."

        try:
            self.atem.disconnect()
        except Exception:
            pass

        self.atem = replacement
        self.labels.atem = self.atem
        return True, f"Configuration saved and reconnected to ATEM at {host}:{port}."
